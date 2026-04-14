from pathlib import Path
import json
import argparse
from tqdm import tqdm

from domain_generation import *      # generate_paths, process_domains, DOMAIN_TYPES
from api_call import call_openrouter
from checker import build_metrics


def main():
    parser = argparse.ArgumentParser(description="LLM Planning + Reasoning Test")
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--domain', type=str, default='folding')
    parser.add_argument('--problem', type=str, default='p01')
    parser.add_argument('--variant', type=str, default='canonical')
    parser.add_argument('--full', action='store_true')

    args = parser.parse_args()

    print("🚀 LLM Planning Pipeline — Reasoning ON/OFF + Metrics")
    print("=" * 100)

    # === ЗАЩИТА ОТ ПЕРЕЗАПИСИ optimal plans ===
    generate_paths(DOMAIN_TYPES, force=False)   # force=False — не трогаем .plan файлы
    process_domains(DOMAIN_TYPES, force=False)

    if args.full or not args.test:
        # ... (полный прогон остаётся без изменений)
        ...
    else:
        # ===================== ТЕСТ =====================
        print(f"\n🧪 ТЕСТ: {args.domain}/{args.problem}/{args.variant}")
        curr_path = Path(f'materials/{args.domain}') / args.problem
        domain_file = curr_path / args.variant / 'domain.pddl'
        problem_file = curr_path / f'{args.problem}.pddl'
        optimal_plan = curr_path / f'{args.problem}.plan'
        domain_dir = curr_path / args.variant
        metrics_path = domain_dir / 'llm_metrics.json'

        meta = {"problem": str(problem_file), "domain_variant": args.variant}

        for reasoning_enabled in [False, True]:
            mode = "reasoning" if reasoning_enabled else "plain"
            print(f"   → Запуск {mode}...")

            res = call_openrouter(domain_file, problem_file, reasoning_enabled=reasoning_enabled)

            filename = 'llm_plan_reasoning.pddl' if reasoning_enabled else 'llm_plan.pddl'
            plan_path = domain_dir / filename

            with open(plan_path, 'w', encoding='utf-8') as f:
                f.write(res['plan'])

            metrics = build_metrics(domain_file, problem_file, plan_path, optimal_plan)

            print(f"   ✅ {filename} сохранён | VAL: {metrics['VAL'][0]}")

            # Сохраняем в общий json
            key = "with_reasoning" if reasoning_enabled else "without_reasoning"
            meta[key] = {
                **{k: v for k, v in res.items() if k != 'plan'},
                "metrics": metrics,
                "plan_file": filename
            }

        # Финальное сохранение метрик
        with open(metrics_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

        print(f"   📊 Метрики сохранены → {metrics_path}")


if __name__ == '__main__':
    main()