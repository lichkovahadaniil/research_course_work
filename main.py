from pathlib import Path
import json
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from domain_generation import *      
from api_call import call_openrouter, supports_reasoning
from checker import build_metrics

MODEL_PROVIDER_MAP = {
    "xiaomi/mimo-v2-flash": "xiaomi/mimo-v2-flash:fp8",
    "qwen/qwen3.5-35b-a3b:alibaba": "qwen/qwen3.5-35b-a3b:alibaba",
}

TEST_MODELS = [
    "openai/gpt-5-mini",
    "x-ai/grok-4.1-fast",
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

def process_single_model(
    model_full: str,
    domain_file: Path,
    problem_file: Path,
    optimal_plan: Path,
    variant_dir: Path,
    force: bool = False,
) -> tuple[str | None, dict | None]:
    short_name = model_full.split('/')[-1].replace(':', '-').replace('.', '-')
    model_dir = variant_dir / short_name
    model_dir.mkdir(parents=True, exist_ok=True)

    plan_path = model_dir / 'llm.plan'
    result_path = model_dir / 'llm_result.json'

    # === КРИТИЧНО: пропуск уже обработанного ===
    if not force and plan_path.exists() and result_path.exists():
        safe_print(f"[{short_name}] ⏭  {variant_dir.name} — уже есть llm.plan, пропуск")
        with open(result_path, encoding='utf-8') as f:
            entry = json.load(f)
        return f"{short_name}_reasoning", entry

    model_to_call = MODEL_PROVIDER_MAP.get(model_full, model_full)
    safe_print(f"[{short_name}] 📌 Запуск → {variant_dir.name} (provider: {model_to_call})")

    try:
        res = call_openrouter(
            domain_file, problem_file, model=model_to_call, reasoning_enabled=True
        )

        with open(plan_path, 'w', encoding='utf-8') as f:
            f.write(res['plan'])

        append_spending(res, model_full, domain_file, problem_file)

        metrics = build_metrics(domain_file, problem_file, plan_path, optimal_plan)

        llm_cost = metrics.get("LLM_COST", {}).get("cost")
        safe_print(f"[{short_name}] ✅ {variant_dir.name}/llm.plan | VAL: {metrics['VAL'][0]} | COST: {llm_cost}")

        key = f"{short_name}_reasoning"
        entry = {**{k: v for k, v in res.items() if k != 'plan'}, "metrics": metrics, "plan_file": str(plan_path)}

        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(entry, f, ensure_ascii=False, indent=2)

        return key, entry

    except Exception as e:
        safe_print(f"[{short_name}] ❌ Ошибка в {variant_dir.name}: {e}")
        return None, None


def run_for_selection(domain: str, problem: str | None = None, variant: str | None = None, force: bool = False, workers: int = 40):
    """Единая функция — обрабатывает любой поднабор materials"""
    domain_path = Path(f"materials/{domain}")
    if not domain_path.exists():
        safe_print(f"❌ Домен {domain} не найден")
        return

    # Собираем все задачи
    tasks = []
    if problem is None:  # весь домен
        prob_dirs = sorted(domain_path.glob("p*"))
    else:
        prob_dirs = [domain_path / problem]

    for prob_dir in prob_dirs:
        if not prob_dir.is_dir():
            continue
        prob_name = prob_dir.name
        problem_file = prob_dir / f"{prob_name}.pddl"
        optimal_plan = prob_dir / f"{prob_name}.plan"

        if variant is None or variant == "all":
            variants = [d for d in prob_dir.iterdir() if d.is_dir() and (d / "domain.pddl").exists()]
        else:
            variants = [prob_dir / variant]

        for v_dir in variants:
            for model_full in TEST_MODELS:
                tasks.append((
                    model_full,
                    v_dir / "domain.pddl",
                    problem_file,
                    optimal_plan,
                    v_dir,
                    force
                ))

    safe_print(f"🚀 Запускаем {len(tasks)} задач (workers={workers})...")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(process_single_model, *task) for task in tasks]
        for _ in as_completed(futures):
            pass

    # После всего — строим summary/metrics
    for prob_dir in (prob_dirs if problem else domain_path.glob("p*")):
        variants = [d for d in prob_dir.iterdir() if d.is_dir() and (d / "domain.pddl").exists()]
        for v_dir in variants:
            build_variant_summary(v_dir)

    build_global_metrics(domain)
    safe_print("🎉 Готово! metric.json обновлён")


def main():
    parser = argparse.ArgumentParser(description="LLM Planning Pipeline — универсальный режим")
    parser.add_argument('--domain', type=str, default='folding')
    parser.add_argument('--problem', type=str, default=None, help='p01 или all (None = весь домен)')
    parser.add_argument('--variant', type=str, default=None, help='canonical / random_05 / all (None = все)')
    parser.add_argument('--workers', type=int, default=40)
    parser.add_argument('--force', action='store_true', help='Перезапускать даже если llm.plan уже есть')

    args = parser.parse_args()

    safe_print("🚀 LLM Planning Pipeline — универсальный запуск")
    safe_print("=" * 140)

    generate_paths(DOMAIN_TYPES, force=False)
    selected_problems = [1, 5, 10, 15, 20]
    process_domains(DOMAIN_TYPES, force=args.force, problems=selected_problems)

    # Предпроверка
    for model_full in TEST_MODELS:
        supports_reasoning(model_full)

    run_for_selection(
        domain=args.domain,
        problem=args.problem,
        variant=args.variant,
        force=args.force,
        workers=args.workers
    )


if __name__ == '__main__':
    main()