from pathlib import Path
from shuffler import shuffle
import re

DOMAIN_TYPES = ['blocksworld', 'rover', 'logistics']

def natural_sort_key(name: str):
    """сортировка: instance-1, instance-2, ..., instance-10"""
    def convert(text):
        return int(text) if text.isdigit() else text.lower()
    return [convert(c) for c in re.split('([0-9]+)', name)]

for domain_name in DOMAIN_TYPES:
    print(f"\n🚀 Generating shuffled domains for {domain_name.upper()}...")

    domain_base = f"domains/original/{domain_name}/domain.pddl"
    instances_dir = Path(f"domains/original/{domain_name}/instances")

    # Получаем все проблемы и сортируем по-человечески
    problem_files = sorted(instances_dir.glob("*.pddl"), key=lambda p: natural_sort_key(p.stem))

    for problem_path in problem_files:
        instance_name = problem_path.stem

        print(f"   Processing {instance_name}...")

        try:
            shuffle(
                domain=domain_base,
                problem=str(problem_path),
                domain_name=domain_name,
                instance_name=instance_name
            )
        except Exception as e:
            print(f"   ❌ Failed on {instance_name}: {type(e).__name__} - {e}")
            continue  # продолжаем дальше, не падаем полностью

print("\n✅ Phase 1 finished — all possible domains generated!")