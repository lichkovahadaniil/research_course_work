import pandas as pd
from pathlib import Path
from datetime import datetime

from api_call import call
from checker import build_metrics

DOMAIN_TYPES = ['blocksworld', 'rover', 'logistics']
MODEL_NAME = "openai/gpt-oss-20b"

RESULTS_DIR = Path("results") / datetime.now().strftime("%Y-%m-%d_%H-%M")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

all_results = []

for domain_name in DOMAIN_TYPES:
    shuffle_dir = Path(f"domains/shuffle/{domain_name}")
    instances_dir = Path(f"domains/original/{domain_name}/instances")

    for shuffled_path in sorted(shuffle_dir.glob("*.pddl")):
        # извлекаем instance_name из имени файла
        stem = shuffled_path.stem
        instance_name = stem.split('_')[-1]   # domain_xxx_instance-5 → instance-5
        shuffle_type = stem.replace(f"_{instance_name}", "").replace("domain_", "")

        problem_path = instances_dir / f"{instance_name}.pddl"

        print(f"   → {domain_name} | {instance_name} | shuffle={shuffle_type}")

        plan_path = f"plans/{domain_name}_{instance_name}_{shuffle_type}.txt"

        try:
            call(domain=str(shuffled_path), problem=str(problem_path), plan_path=plan_path)
        except Exception as e:
            print(f"      ❌ API error: {e}")
            continue

        metrics = build_metrics(
            dmain_path=str(shuffled_path),
            problem_path=str(problem_path),
            plan_path=plan_path
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
            "plan_path": plan_path,
            "domain_path": str(shuffled_path)
        }
        all_results.append(result_row)

# Save
df = pd.DataFrame(all_results)
csv_path = RESULTS_DIR / "full_results.csv"
df.to_csv(csv_path, index=False)

print("\n✅ EVALUATION FINISHED!")
print(df.groupby(['domain', 'shuffle_type'])['valid_VAL', 'gap'].mean().round(4))