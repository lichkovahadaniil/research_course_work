import os
import pandas as pd
from pathlib import Path
from datetime import datetime

from api_call import call
from checker import build_metrics
from shuffler import shuffle
from vars import *

# ====================== CONFIG ======================
DOMAIN_TYPES = ['blocksworld', 'rover', 'logistics']
MODEL_NAME = "openai/gpt-oss-20b"
TEMPERATURE = 0.0

RESULTS_DIR = Path("results") / datetime.now().strftime("%Y-%m-%d_%H-%M")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

all_results = []

for domain_name in DOMAIN_TYPES:
    print(f"\n🚀 Starting per-instance experiment for {domain_name.upper()}...")

    domain_base = f"domains/original/{domain_name}/domain.pddl"
    instances_dir = Path(f"domains/original/{domain_name}/instances")
    shuffle_dir = Path(f"domains/shuffle/{domain_name}")
    shuffle_dir.mkdir(parents=True, exist_ok=True)

    for problem_path in sorted(instances_dir.glob("*.pddl")):
        instance_name = problem_path.stem
        print(f"\n   Processing instance: {instance_name}")

        # 1. Генерируем все shuffled-домены именно для этой instance
        shuffle(
            domain=domain_base,
            problem=str(problem_path),
            domain_name=domain_name,
            instance_name=instance_name
        )

        # 2. Собираем все сгенерированные домены для этой instance
        shuffled_domains = list(shuffle_dir.glob(f"*_{instance_name}.pddl"))

        for shuffled_path in sorted(shuffled_domains):
            shuffle_type = shuffled_path.stem.replace(f"_{instance_name}", "").replace("domain_", "")

            print(f"      → shuffle={shuffle_type} | model={MODEL_NAME}")

            plan_path = f"plans/{domain_name}_{instance_name}_{shuffle_type}.txt"

            # 3. LLM call (твоя 20B GPT)
            try:
                plan_text = call(
                    domain=str(shuffled_path),
                    problem=str(problem_path),
                    plan_path=plan_path
                )
            except Exception as e:
                print(f"      ❌ API error: {e}")
                continue

            # 4. Метрики
            metrics = build_metrics(
                dmain_path=str(shuffled_path),
                problem_path=str(problem_path),
                plan_path=plan_path
            )

            # 5. Результат
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

# ====================== SAVE ======================
df = pd.DataFrame(all_results)
csv_path = RESULTS_DIR / "full_per_instance_results.csv"
df.to_csv(csv_path, index=False)

summary = df.groupby(['domain', 'shuffle_type']).agg({
    'valid_VAL': 'mean',
    'gap': ['mean', 'std'],
    'llm_cost': 'mean'
}).round(4)

print("\n" + "="*90)
print("✅ PER-INSTANCE EXPERIMENT FINISHED!")
print(summary)
summary.to_csv(RESULTS_DIR / "summary_per_instance.csv")

print(f"\nFull results → {csv_path}")