from pathlib import Path
from shuffler import shuffle
import re

DOMAIN_TYPES = ['blocksworld', 'rover', 'logistics']

def natural_sort_key(name: str):
    """Human-friendly sort: instance-1, instance-2, ..., instance-10, instance-11..."""
    def convert(text):
        return int(text) if text.isdigit() else text.lower()
    return [convert(c) for c in re.split('([0-9]+)', name)]

def is_instance_fully_generated(domain_name: str, instance_name: str) -> bool:
    """Проверяем, есть ли все 5 доменов для этой инстансы"""
    shuffle_dir = Path(f"domains/shuffle/{domain_name}")
    patterns = [
        f"domain_canonical_{instance_name}.pddl",
        f"domain_optimal_{instance_name}.pddl",
        f"domain_frequency_{instance_name}.pddl",
        f"domain_dispersion_{instance_name}.pddl",
        f"domain_random_dispersion_source_{instance_name}.pddl"
    ]
    return all((shuffle_dir / p).exists() for p in patterns)

for domain_name in DOMAIN_TYPES:
    print(f"\n🚀 Generating shuffled domains for {domain_name.upper()}...")

    domain_base = f"domains/original/{domain_name}/domain.pddl"
    instances_dir = Path(f"domains/original/{domain_name}/instances")

    # Все возможные инстансы в правильном порядке
    all_problem_files = sorted(
        instances_dir.glob("*.pddl"),
        key=lambda p: natural_sort_key(p.stem)
    )

    # Находим последнюю полностью обработанную инстансу
    start_from = 0
    for idx, problem_path in enumerate(all_problem_files):
        instance_name = problem_path.stem
        if is_instance_fully_generated(domain_name, instance_name):
            start_from = idx + 1
        else:
            break  # как только нашли первую неготовую — начинаем с неё

    print(f"   Resuming from instance index {start_from} "
          f"(already done: {start_from} instances)")

    for problem_path in all_problem_files[start_from:]:
        instance_name = problem_path.stem
        print(f"   → {instance_name}")

        try:
            shuffle(
                domain=domain_base,
                problem=str(problem_path),
                domain_name=domain_name,
                instance_name=instance_name
            )
        except Exception as e:
            print(f"   ❌ Failed on {instance_name}: {type(e).__name__} — {e}")
            continue

print("\n✅ Phase 1 finished — resume completed!")