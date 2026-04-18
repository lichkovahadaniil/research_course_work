import shutil
from pathlib import Path
from shuffler import shuffle

# Список доменов
DOMAIN_TYPES = ['folding', 'labyrinth', 'recharging-robots', 'ricochet-robots', 'rubiks-cube']

def generate_paths(domains, force: bool = False):
    for d in domains:
        src_path = Path(f'ipc2023-dataset-main/opt/{d}')
        dest_path = Path(f'materials/{d}')

        dest_path.mkdir(parents=True, exist_ok=True)

        domain_dest = dest_path / 'domain.pddl'
        if force or not domain_dest.exists():
            shutil.copy(src_path / 'domain.pddl', domain_dest)

        for i in range(1, 21):
            name = f'p{i:02d}'
            subfolder = dest_path / name
            subfolder.mkdir(exist_ok=True)

            problem_dest = subfolder / f'{name}.pddl'
            plan_dest = subfolder / f'{name}.plan'

            if force or not problem_dest.exists():
                shutil.copy(src_path / f'{name}.pddl', problem_dest)

            if not plan_dest.exists():
                shutil.copy(src_path / f'{name}.plan', plan_dest)
                print(f"   → {name}.plan скопирован (впервые)")
            else:
                print(f"   → {name}.plan уже существует — защищён от перезаписи")


def process_domains(domains, force: bool = False, problems: list[int] | None = None):
    """
    Запускает shuffle для указанных проблем.
    problems=None → все 20 проблем
    problems=[1,5,10,15,20] → только эти 5
    """
    if problems is None:
        problems = list(range(1, 21))
    else:
        problems = sorted(set(problems))

    total_problems = len(domains) * len(problems)
    processed = 0
    skipped = 0

    for d in domains:
        src_path = Path(f'materials/{d}')
        domain_file = src_path / 'domain.pddl'
        
        print(f"\n🔄 Домен: {d}  ({len(problems)} проблем)")

        for i in problems:
            name = f'p{i:02d}'
            problem_file = src_path / name / f'{name}.pddl'
            optimal_plan_file = src_path / name / f'{name}.plan'
            shuffle_path = src_path / name

            already_shuffled = (shuffle_path / 'canonical').exists()

            if already_shuffled and not force:
                print(f"   ⏭  {name} — уже обработан, пропуск")
                skipped += 1
            else:
                if already_shuffled and force:
                    print(f"   ♻️  {name} — force=True, пересоздаём shuffle")
                else:
                    print(f"   ▶️  {name} — генерация 9 вариантов...")
                
                shuffle(domain_file, problem_file, optimal_plan_file, shuffle_path)
                processed += 1

    print(f"\n{'='*80}")
    print(f"✅ process_domains завершён!")
    print(f"   Обработано: {processed} проблем")
    print(f"   Пропущено: {skipped} проблем")
    print(f"   Всего проблем в датасете: {total_problems}")
    if force:
        print("   ⚠️  Режим force=True — все shuffle пересозданы")