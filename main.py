from pathlib import Path
import json
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from domain_generation import *      # generate_paths, process_domains, DOMAIN_TYPES
from api_call import call_openrouter, supports_reasoning
from checker import build_metrics

TEST_MODELS = [
    "openai/gpt-5-mini",
    "x-ai/grok-4.1-fast",
    "deepseek/deepseek-v3.2",
    "google/gemma-4-31b-it",
    "xiaomi/mimo-v2-flash",
    "qwen/qwen3.5-35b-a3b:alibaba",
]

print_lock = threading.Lock()
spendings_lock = threading.Lock()


def safe_print(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)


def append_spending(res: dict, model: str, domain_file: Path, problem_file: Path):
    spendings_path = Path("spendings.json")
    spendings_path.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "domain": str(domain_file),
        "problem": str(problem_file),
        "prompt_tokens": res.get("prompt_tokens"),
        "completion_tokens": res.get("completion_tokens"),
        "total_tokens": res.get("total_tokens"),
        "duration_sec": res.get("duration_sec"),
    }

    with spendings_lock:
        data = []
        if spendings_path.exists():
            try:
                with open(spendings_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except:
                pass
        data.append(entry)
        with open(spendings_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def process_single_model(
    model_full: str,
    domain_file: Path,
    problem_file: Path,
    optimal_plan: Path,
    variant_dir: Path,
) -> tuple[str | None, dict | None]:
    short_name = model_full.split('/')[-1].replace(':', '-').replace('.', '-')
    model_dir = variant_dir / short_name
    model_dir.mkdir(parents=True, exist_ok=True)

    safe_print(f"[{short_name}] 📌 Запуск → {variant_dir.name}")

    try:
        res = call_openrouter(
            domain_file, problem_file, model=model_full, reasoning_enabled=True
        )

        plan_path = model_dir / 'llm.plan'
        with open(plan_path, 'w', encoding='utf-8') as f:
            f.write(res['plan'])

        append_spending(res, model_full, domain_file, problem_file)

        metrics = build_metrics(domain_file, problem_file, plan_path, optimal_plan)

        llm_cost = metrics.get("LLM_COST", {}).get("cost")
        safe_print(f"[{short_name}] ✅ {variant_dir.name}/llm.plan | VAL: {metrics['VAL'][0]} | COST: {llm_cost}")

        key = f"{short_name}_reasoning"
        entry = {
            **{k: v for k, v in res.items() if k != 'plan'},
            "metrics": metrics,
            "plan_file": str(plan_path)
        }
        return key, entry

    except Exception as e:
        safe_print(f"[{short_name}] ❌ Ошибка в {variant_dir.name}: {e}")
        return None, None


def build_global_metrics(domain: str):
    """Собирает materials/metric.json со всей структурой"""
    metric_path = Path("materials") / "metric.json"
    metric = {}
    if metric_path.exists():
        try:
            with open(metric_path, encoding='utf-8') as f:
                metric = json.load(f)
        except:
            pass

    if domain not in metric:
        metric[domain] = {}

    domain_path = Path(f"materials/{domain}")
    for prob_dir in sorted(domain_path.glob("p*")):
        if not prob_dir.is_dir():
            continue
        prob_name = prob_dir.name
        metric[domain][prob_name] = {}

        for variant_dir in sorted(prob_dir.iterdir()):
            if not variant_dir.is_dir() or not (variant_dir / "domain.pddl").exists():
                continue
            variant_name = variant_dir.name

            summary_path = variant_dir / "llm_summary.json"
            if summary_path.exists():
                with open(summary_path, encoding='utf-8') as f:
                    variant_summary = json.load(f)
                metric[domain][prob_name][variant_name] = variant_summary

    with open(metric_path, 'w', encoding='utf-8') as f:
        json.dump(metric, f, ensure_ascii=False, indent=2)
    safe_print(f"📊 Обновлён глобальный metric.json ({len(metric[domain])} проблем)")


def main():
    parser = argparse.ArgumentParser(description="LLM Planning Pipeline — Multi-Model + Reasoning")
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--domain', type=str, default='folding')
    parser.add_argument('--problem', type=str, default='p01')
    parser.add_argument('--variant', type=str, default='canonical')
    parser.add_argument('--full', action='store_true')

    args = parser.parse_args()

    safe_print("🚀 LLM Planning Pipeline — FULL MODE + 6 моделей + 30 parallel + global metric.json")
    safe_print("=" * 130)

    generate_paths(DOMAIN_TYPES, force=False)
    process_domains(DOMAIN_TYPES, force=False)

    # === 0. Предпроверка reasoning (один раз) ===
    safe_print("🔍 Предпроверка capabilities...")
    for model_full in TEST_MODELS:
        supports_reasoning(model_full)
    safe_print("✅ Кэш готов.\n")

    if args.full:
        # ===================== FULL MODE =====================
        safe_print(f"🔥 FULL RUN для домена: {args.domain} (20 проблем × 14 вариантов × 6 моделей)\n")
        domain_path = Path(f"materials/{args.domain}")

        for i in range(1, 21):
            prob_name = f"p{i:02d}"
            prob_dir = domain_path / prob_name
            if not prob_dir.exists():
                continue

            problem_file = prob_dir / f"{prob_name}.pddl"
            optimal_plan = prob_dir / f"{prob_name}.plan"

            # Все варианты домена для этой проблемы
            variants = [d for d in prob_dir.iterdir() if d.is_dir() and (d / "domain.pddl").exists()]

            safe_print(f"📦 {prob_name} → {len(variants)} вариантов × 6 моделей = {len(variants)*len(TEST_MODELS)} вызовов")

            tasks = []
            for variant_dir in variants:
                for model_full in TEST_MODELS:
                    tasks.append((model_full, variant_dir / "domain.pddl", problem_file, optimal_plan, variant_dir))

            # Максимальный параллелизм
            with ThreadPoolExecutor(max_workers=30) as executor:
                futures = [executor.submit(process_single_model, *task) for task in tasks]
                for _ in as_completed(futures):
                    pass  # просто ждём завершения

            safe_print(f"✅ {prob_name} завершён\n")

        build_global_metrics(args.domain)
        safe_print("🎉 FULL RUN ЗАВЕРШЁН. metric.json готов.")
        
    # ===================== ТЕСТ =====================
    else:
        safe_print(f"\n🧪 ТЕСТ: {args.domain}/{args.problem}/{args.variant}\n")

        curr_path = Path(f'materials/{args.domain}') / args.problem
        domain_file = curr_path / args.variant / 'domain.pddl'
        problem_file = curr_path / f'{args.problem}.pddl'
        optimal_plan = curr_path / f'{args.problem}.plan'
        variant_dir = curr_path / args.variant

        # === 1. Предпроверка reasoning (теперь правильно импортирована) ===
        safe_print("🔍 Предпроверка capabilities reasoning для всех моделей...")
        for model_full in TEST_MODELS:
            supports_reasoning(model_full)          # ← теперь работает корректно
        safe_print("✅ Все модели проверены. Кэш model_capabilities.json обновлён.\n")

        safe_print(f"🚀 Запускаем параллельно {len(TEST_MODELS)} моделей (reasoning only)...\n")

        results = []
        with ThreadPoolExecutor(max_workers=len(TEST_MODELS)) as executor:
            futures = [
                executor.submit(
                    process_single_model,
                    model_full, domain_file, problem_file, optimal_plan, variant_dir
                )
                for model_full in TEST_MODELS
            ]
            for future in as_completed(futures):
                key, entry = future.result()
                if key and entry:
                    results.append((key, entry))

        build_global_metrics(args.domain)

    # === 2. Свежий metrics.json (без старого мусора) ===
    meta = {
        "problem": str(problem_file),
        "domain_variant": args.variant,
        "test_models": TEST_MODELS
    }
    for key, entry in results:
        meta[key] = entry

    metrics_path = variant_dir / 'llm_metrics.json'
    with open(metrics_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

# === 3. Сводный summary.json + таблица ===
    summary = {}
    for key, value in meta.items():
        if not isinstance(value, dict) or "metrics" not in value:
            continue
        m = value["metrics"]
        order_m = m.get("ORDER_METRIC") or {}
        llm_cost_dict = m.get("LLM_COST") or {}

        short_name = key.replace('_reasoning', '')

        summary[short_name] = {
            "valid": m.get("VAL", (False, ""))[0],
            "llm_cost": llm_cost_dict.get("cost"),           # ← настоящая стоимость
            "llm_actions_len": llm_cost_dict.get("num_actions"),  # ← длина
            "optimal_cost": m.get("OPTIMAL_COST"),
            "cost_gap_%": round(m.get("GAP", 0) * 100, 2) if m.get("GAP") is not None else None,
            "order_distance_norm": order_m.get("normalized_distance"),
            "kendall_inversions": order_m.get("kendall_tau_inversions"),
            "insertions": order_m.get("insertions"),
            "deletions": order_m.get("deletions"),
            "duration_sec": value.get("duration_sec"),
            "total_tokens": value.get("total_tokens"),
        }

    summary_path = variant_dir / 'llm_summary.json'
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

# === 4. Красивая таблица (добавлена колонка LEN) ===
    safe_print("\n" + "=" * 140)
    safe_print("📊 СВОДНАЯ ТАБЛИЦА (reasoning only — cost = Final value / Optimal cost)")
    safe_print("=" * 140)
    safe_print(f"{'Модель':<20} {'VALID':<6} {'COST':<8} {'LEN':<6} {'GAP%':<8} {'ORD_DIST':<10} {'DUR(s)':<8} {'TOKENS':<9}")
    safe_print("-" * 140)
    for model, s in summary.items():
        valid_str = "✅" if s["valid"] else "❌"
        cost_str = f"{s['llm_cost']:.2f}" if s['llm_cost'] is not None else "N/A"
        len_str = str(s['llm_actions_len']) if s['llm_actions_len'] is not None else "N/A"
        gap_str = f"{s['cost_gap_%']:.1f}%" if s['cost_gap_%'] is not None else "N/A"
        ord_str = f"{s['order_distance_norm']:.4f}" if s['order_distance_norm'] is not None else "N/A"
        dur_str = f"{s['duration_sec']:.1f}" if s['duration_sec'] is not None else "N/A"
        tokens_str = str(s['total_tokens']) if s['total_tokens'] is not None else "N/A"

        safe_print(f"{model:<20} {valid_str:<6} {cost_str:<8} {len_str:<6} {gap_str:<8} {ord_str:<10} {dur_str:<8} {tokens_str:<9}")
    safe_print("=" * 140)
    safe_print(f"🎉 Тест завершён!")
    safe_print(f"   📁 Метрики   → {metrics_path}")
    safe_print(f"   📈 Сводка    → {summary_path}")


if __name__ == '__main__':
    main()