from pathlib import Path
import json
import argparse
from tqdm import tqdm

from domain_generation import *      # generate_paths, process_domains, DOMAIN_TYPES
from api_call import call_openrouter, supports_reasoning
from checker import build_metrics


TEST_MODELS = [
    "openai/gpt-5-mini",
    "openai/gpt-5-nano",
    "google/gemma-4-31b-it:nitro",
    "deepseek/deepseek-v3.2",
]


def main():
    parser = argparse.ArgumentParser(description="LLM Planning Pipeline — Multi-Model + Reasoning")
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--domain', type=str, default='folding')
    parser.add_argument('--problem', type=str, default='p01')
    parser.add_argument('--variant', type=str, default='canonical')
    parser.add_argument('--full', action='store_true')

    args = parser.parse_args()

    print("🚀 LLM Planning Pipeline — Multi-Model + Reasoning + Order Metrics")
    print("=" * 110)

    generate_paths(DOMAIN_TYPES, force=False)
    process_domains(DOMAIN_TYPES, force=False)

    if args.full or not args.test:
        
        return

# ... (верхняя часть без изменений)

    else:
        # ===================== ТЕСТ =====================
        print(f"\n🧪 ТЕСТ: {args.domain}/{args.problem}/{args.variant}\n")

        curr_path = Path(f'materials/{args.domain}') / args.problem
        domain_file = curr_path / args.variant / 'domain.pddl'
        problem_file = curr_path / f'{args.problem}.pddl'
        optimal_plan = curr_path / f'{args.problem}.plan'
        variant_dir = curr_path / args.variant

        for model_full in TEST_MODELS:
            short_name = model_full.split('/')[-1].replace(':', '-').replace('.', '-')
            model_dir = variant_dir / short_name
            model_dir.mkdir(parents=True, exist_ok=True)

            print(f"📌 Модель: {short_name} ({model_full})")

            # Только один вызов, если reasoning не поддерживается
            for reasoning_enabled in [False, True]:
                if reasoning_enabled and not supports_reasoning(model_full):  # используем кэш
                    continue  # пропускаем, если не поддерживает

                mode = "reasoning" if reasoning_enabled else "plain"
                try:
                    res = call_openrouter(domain_file, problem_file, model=model_full, reasoning_enabled=reasoning_enabled)

                    filename = 'llm_reasoning.plan' if res["reasoning_enabled"] else 'llm_plan.plan'
                    plan_path = model_dir / filename

                    with open(plan_path, 'w', encoding='utf-8') as f:
                        f.write(res['plan'])
                        print('AAAAA', res['plan'][:20])

                    metrics = build_metrics(domain_file, problem_file, plan_path, optimal_plan)

                    print(f"   ✅ {filename} | VAL: {metrics['VAL'][0]}")

                    # Сохранение метрик
                    metrics_path = variant_dir / 'llm_metrics.json'
                    if metrics_path.exists():
                        with open(metrics_path, 'r', encoding='utf-8') as f:
                            meta = json.load(f)
                    else:
                        meta = {"problem": str(problem_file), "domain_variant": args.variant}

                    key = f"{short_name}_{mode}"
                    meta[key] = {
                        **{k: v for k, v in res.items() if k != 'plan'},
                        "metrics": metrics,
                        "plan_file": str(plan_path)
                    }

                    with open(metrics_path, 'w', encoding='utf-8') as f:
                        json.dump(meta, f, ensure_ascii=False, indent=2)

                except Exception as e:
                    print(f"   ❌ Ошибка {short_name} {mode}: {e}")

    print(f"\n🎉 Тест завершён.")


if __name__ == '__main__':
    main()