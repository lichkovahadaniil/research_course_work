import pandas as pd
from pathlib import Path
from datetime import datetime
from generate_all_shuffled_domains import natural_sort_key
from api_call import call
from checker import build_metrics

DOMAIN_TYPES = ['blocksworld', 'rover', 'logistics']
MODEL_NAME = "llama-3.3-70b-versatile"

RESULTS_DIR = Path("results") / datetime.now().strftime("%Y-%m-%d_%H-%M")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

PLANS_BASE = Path("plans")
PLANS_BASE.mkdir(parents=True, exist_ok=True)

all_results = []

for domain_name in DOMAIN_TYPES:
    shuffle_dir = Path(f"domains/shuffle/{domain_name}")
    if not shuffle_dir.exists():
        continue

    print(f"\n🚀 Evaluating {domain_name.upper()}...")

    # Новое: итерируемся по папкам-инстансам
    for instance_dir in sorted(shuffle_dir.iterdir(), key=lambda d: natural_sort_key(d.name) if d.is_dir() else ""):
        if not instance_dir.is_dir():
            continue
        instance_name = instance_dir.name

        problem_path = Path(f"domains/original/{domain_name}/instances/{instance_name}.pddl")
        if not problem_path.exists():
            continue

        domain_plans_dir = PLANS_BASE / domain_name
        domain_plans_dir.mkdir(parents=True, exist_ok=True)

        for shuffled_path in sorted(instance_dir.glob("domain_*.pddl")):
            stem = shuffled_path.stem.replace("domain_", "")

            if stem == "canonical":          shuffle_type = "canonical"
            elif stem == "optimal":          shuffle_type = "optimal"
            elif stem == "frequency":        shuffle_type = "frequency"
            elif stem == "dispersion":       shuffle_type = "dispersion"
            elif stem == "random_dispersion_source": shuffle_type = "random_dispersion_source"
            else:                            shuffle_type = "unknown"

            print(f"   → {instance_name} | {shuffle_type}")

            plan_path = domain_plans_dir / f"{instance_name}_{shuffle_type}.txt"

            try:
                call(domain=str(shuffled_path), problem=str(problem_path), plan_path=str(plan_path))
            except Exception as e:
                print(f"      ❌ API error: {e}")
                continue

        optimal_plan_path = f"plans/optimal/{domain_name}_{instance_name}.txt"

        metrics = build_metrics(
            dmain_path=str(shuffled_path),
            problem_path=str(problem_path),
            plan_path=str(plan_path),
            optimal_plan_path=optimal_plan_path
        )
        result_row = {
            "domain": domain_name,
            "instance": instance_name,
            "shuffle_type": shuffle_type,
            "model": MODEL_NAME,
            "valid_VAL": metrics['VAL'][0] if isinstance(metrics['VAL'], tuple) else False,
            "llm_cost": metrics['FD'].get('llm_cost'),
            "optimal_cost": metrics['FD'].get('optimal_cost'),
            "gap": metrics['FD'].get('gap'),
            "timestamp": datetime.now().isoformat(),
            "plan_path": str(plan_path),
            "domain_path": str(shuffled_path)
        }
        all_results.append(result_row)

# Сохраняем результаты (даже если часть упала)
df = pd.DataFrame(all_results)
csv_path = RESULTS_DIR / "results.csv"
df.to_csv(csv_path, index=False)

summary = df.groupby(['domain', 'shuffle_type']).agg({
    'valid_VAL': 'mean',
    'gap': ['mean', 'std'],
    'llm_cost': 'mean'
}).round(4)

print("\n" + "="*80)
print("✅ EVALUATION FINISHED!")
print(summary)
summary.to_csv(RESULTS_DIR / "summary.csv")

print(f"\nПланы лежат в: plans/{domain_name}/")
print(f"Результаты: {csv_path}")