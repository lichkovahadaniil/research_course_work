from pathlib import Path
import json
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from domain_generation import *      # generate_paths, process_domains, DOMAIN_TYPES
from api_call import call_openrouter, supports_reasoning
from checker import build_metrics

MODEL_PROVIDER_MAP = {
    "xiaomi/mimo-v2-flash": "xiaomi/mimo-v2-flash:fp8",
    "deepseek/deepseek-v3.2": "deepseek/deepseek-v3.2:novita/fp8", 
    "qwen/qwen3.5-35b-a3b:alibaba": "qwen/qwen3.5-35b-a3b:alibaba",
}

TEST_MODELS = [
    "openai/gpt-5-mini",
    "x-ai/grok-4.1-fast",
    "deepseek/deepseek-v3.2",
    # "google/gemma-4-31b-it",
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

def build_variant_summary(variant_dir: Path):
    """Создаёт llm_summary.json + llm_metrics.json для одного варианта (работает и в test, и в full)"""
    summary = {}
    meta = {"problem": None, "domain_variant": variant_dir.name, "test_models": TEST_MODELS}

    for model_dir in sorted(variant_dir.iterdir()):
        if not model_dir.is_dir():
            continue
        result_path = model_dir / "llm_result.json"
        if not result_path.exists():
            continue

        with open(result_path, encoding='utf-8') as f:
            entry = json.load(f)

        m = entry["metrics"]
        order_m = m.get("ORDER_METRIC") or {}
        llm_cost_dict = m.get("LLM_COST") or {}
        short_name = model_dir.name

        summary[short_name] = {
            "valid": m.get("VAL", (False, ""))[0],
            "llm_cost": llm_cost_dict.get("cost"),
            "llm_actions_len": llm_cost_dict.get("num_actions"),
            "optimal_cost": m.get("OPTIMAL_COST"),
            "cost_gap_%": round(m.get("GAP", 0) * 100, 2) if m.get("GAP") is not None else None,
            "bug_optimal": m.get("BUG_OPTIMAL", False),
            "bug_notes": llm_cost_dict.get("notes"),
            "order_distance_norm": order_m.get("normalized_distance"),
            "kendall_inversions": order_m.get("kendall_tau_inversions"),
            "insertions": order_m.get("insertions"),
            "deletions": order_m.get("deletions"),
            "duration_sec": entry.get("duration_sec"),
            "total_tokens": entry.get("total_tokens"),
        }

        if meta["problem"] is None:
            meta["problem"] = entry.get("problem")  # любой, они одинаковые

        meta[short_name + "_reasoning"] = entry

    # llm_summary.json
    with open(variant_dir / 'llm_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    # llm_metrics.json
    with open(variant_dir / 'llm_metrics.json', 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    return summary

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

    # ← НОВОЕ: принудительно используем нужный провайдер/fp8
    model_to_call = MODEL_PROVIDER_MAP.get(model_full, model_full)

    safe_print(f"[{short_name}] 📌 Запуск → {variant_dir.name} (provider: {model_to_call})")

    try:
        res = call_openrouter(
            domain_file, problem_file, model=model_to_call, reasoning_enabled=True
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

        # ← НОВОЕ: сохраняем результат модели (нужно для full-режима)
        with open(model_dir / "llm_result.json", 'w', encoding='utf-8') as f:
            json.dump(entry, f, ensure_ascii=False, indent=2)

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
    parser = argparse.ArgumentParser(...)
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--domain', type=str, default='folding')
    parser.add_argument('--problem', type=str, default='p01')
    parser.add_argument('--variant', type=str, default='canonical')
    parser.add_argument('--full', action='store_true')
    parser.add_argument('--workers', type=int, default=30)
    parser.add_argument('--all-variants', action='store_true',
                        help='В тестовом режиме обработать ВСЕ 14 вариантов для указанной проблемы')

    args = parser.parse_args()

    safe_print("🚀 LLM Planning Pipeline — FULL MODE + provider mapping + per-variant summaries")
    safe_print("=" * 140)

    generate_paths(DOMAIN_TYPES, force=False)
    process_domains(DOMAIN_TYPES, force=False)

    # Предпроверка reasoning
    safe_print("🔍 Предпроверка capabilities...")
    for model_full in TEST_MODELS:
        supports_reasoning(model_full)
    safe_print("✅ Кэш готов.\n")

    if args.full:
        safe_print(f"🔥 FULL RUN для домена: {args.domain} (workers={args.workers})\n")
        domain_path = Path(f"materials/{args.domain}")

        for i in range(1, 21):
            prob_name = f"p{i:02d}"
            prob_dir = domain_path / prob_name
            if not prob_dir.exists():
                continue

            problem_file = prob_dir / f"{prob_name}.pddl"
            optimal_plan = prob_dir / f"{prob_name}.plan"

            variants = [d for d in prob_dir.iterdir() if d.is_dir() and (d / "domain.pddl").exists()]

            safe_print(f"📦 {prob_name} → {len(variants)} вариантов × {len(TEST_MODELS)} моделей")

            tasks = []
            for variant_dir in variants:
                for model_full in TEST_MODELS:
                    tasks.append((model_full, variant_dir / "domain.pddl", problem_file, optimal_plan, variant_dir))

            with ThreadPoolExecutor(max_workers=args.workers) as executor:
                futures = [executor.submit(process_single_model, *task) for task in tasks]
                for _ in as_completed(futures):
                    pass

            # ← НОВОЕ: после всех моделей строим summary для КАЖДОГО варианта
            safe_print(f"📊 Генерируем llm_summary.json для {prob_name}...")
            for variant_dir in variants:
                build_variant_summary(variant_dir)

            safe_print(f"✅ {prob_name} завершён\n")

        build_global_metrics(args.domain)
        safe_print("🎉 FULL RUN ЗАВЕРШЁН. metric.json готов.")
    # ===================== ТЕСТ =====================
    else:
        safe_print(f"\n🧪 ТЕСТ: {args.domain}/{args.problem} {'(все 14 вариантов)' if args.all_variants else args.variant}\n")

        curr_path = Path(f'materials/{args.domain}') / args.problem
        problem_file = curr_path / f'{args.problem}.pddl'
        optimal_plan = curr_path / f'{args.problem}.plan'

        if args.all_variants:
            variants = [d for d in curr_path.iterdir() 
                        if d.is_dir() and (d / "domain.pddl").exists()]
            safe_print(f"📦 Найдено {len(variants)} вариантов → полный параллелизм {len(variants)*len(TEST_MODELS)} задач\n")
        else:
            variant_dir = curr_path / args.variant
            variants = [variant_dir]
            safe_print(f"📦 Один вариант: {args.variant}\n")

        # === ПОЛНЫЙ ПАРАЛЛЕЛИЗМ КАК В FULL-РЕЖИМЕ ===
        tasks = []
        for variant_dir in variants:
            for model_full in TEST_MODELS:
                tasks.append((
                    model_full,
                    variant_dir / "domain.pddl",
                    problem_file,
                    optimal_plan,
                    variant_dir
                ))

        safe_print(f"🚀 Запускаем {len(tasks)} запросов параллельно (workers={args.workers})...\n")

        results = []  # собираем только для последней таблицы (если нужно)
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = [executor.submit(process_single_model, *task) for task in tasks]
            for future in as_completed(futures):
                key, entry = future.result()
                if key and entry:
                    results.append((key, entry))

        # После всех запросов строим summary/metrics для КАЖДОГО варианта
        safe_print(f"\n📊 Генерируем llm_summary.json + llm_metrics.json для всех вариантов...")
        for variant_dir in variants:
            build_variant_summary(variant_dir)
            safe_print(f"   ✅ {variant_dir.name} → файлы готовы")

        build_global_metrics(args.domain)

        # Для таблицы в конце используем последний вариант (или можно убрать таблицу в all-variants)
        variant_dir = variants[-1]  # просто берём последний для таблицы

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
    summary = build_variant_summary(variant_dir)

# === 4. Красивая таблица (добавлена колонка LEN) ===
    safe_print("\n" + "=" * 140)
    safe_print(f"{'Модель':<20} {'VALID':<6} {'COST':<8} {'LEN':<6} {'GAP%':<8} {'ORD_DIST':<10} {'DUR(s)':<8} {'TOKENS':<9}")
    safe_print("-" * 140)

    improvements = []
    for model, s in summary.items():
        valid_str = "✅" if s["valid"] else "❌"
        cost_str = f"{s['llm_cost']:.2f}" if s['llm_cost'] is not None else "N/A"
        len_str = str(s['llm_actions_len']) if s['llm_actions_len'] is not None else "N/A"
        bug_str = "bug" if s.get("bug_optimal") else "clear"
        gap_str = f"{s['cost_gap_%']:+.1f}%" if s['cost_gap_%'] is not None else "N/A"
        ord_str = f"{s['order_distance_norm']:.4f}" if s['order_distance_norm'] is not None else "N/A"
        dur_str = f"{s['duration_sec']:.1f}" if s['duration_sec'] is not None else "N/A"
        tokens_str = str(s['total_tokens']) if s['total_tokens'] is not None else "N/A"
        if s.get("super_optimal"):
            improvements.append({
                "domain": args.domain,
                "problem": args.problem,
                "variant": args.variant,
                "model": model,
                "llm_cost": s["llm_cost"],
                "optimal_cost": s["optimal_cost"],
                "gap_%": s["cost_gap_%"],
                "plan_path": str(variant_dir / f"{model.replace(':', '-')}_reasoning/llm.plan")  # адаптировать
            })
    

        safe_print(f"{model:<20} {valid_str:<6} {cost_str:<8} {len_str:<6} {bug_str:<6} {gap_str:<8} {ord_str:<10} {dur_str:<8} {tokens_str:<9}")
    
    if improvements:
        imp_path = Path("discovered_improvements.json")
        data = []
        if imp_path.exists():
            data = json.loads(imp_path.read_text(encoding='utf-8'))
        data.extend(improvements)
        imp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        safe_print(f"🚀 Найдено {len(improvements)} super-optimal планов! → {imp_path}")

    safe_print("🎉 FULL RUN ЗАВЕРШЁН. metric.json готов.")
    safe_print("=" * 140)
    safe_print(f"🎉 Тест завершён!")
    safe_print(f"   📁 Метрики   → {metrics_path}")


if __name__ == '__main__':
    main()