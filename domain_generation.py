import shutil
from pathlib import Path
from shuffler import shuffle

# Список доменов
DOMAIN_TYPES = ['folding', 'labyrinth', 'recharging-robots', 'ricochet-robots', 'rubiks-cube']

def generate_paths(domains, force: bool = False):
    """
    Создаёт базовую структуру materials/
    
    force=False (по умолчанию) — безопасный режим:
        • если папки p01..p20 уже существуют — ничего не перезаписываем
        • если domain.pddl уже лежит в materials/{d}/ — тоже не трогаем
    
    force=True — полностью пересоздаём (перезаписываем всё)
    """
    for d in domains:
        src_path = Path(f'ipc2023-dataset-main/opt/{d}')
        dest_path = Path(f'materials/{d}')

        dest_path.mkdir(parents=True, exist_ok=True)

        # Копируем domain.pddl в корень домена
        domain_dest = dest_path / 'domain.pddl'
        if force or not domain_dest.exists():
            shutil.copy(src_path / 'domain.pddl', domain_dest)
            print(f"   → domain.pddl {'перезаписан' if domain_dest.exists() else 'скопирован'} для {d}")
        else:
            print(f"   → domain.pddl для {d} уже существует (force=False)")

        # Создаём/обновляем p01..p20
        for i in range(1, 21):
            name = f'p{i:02d}'
            subfolder = dest_path / name
            subfolder.mkdir(exist_ok=True)

            problem_dest = subfolder / f'{name}.pddl'
            plan_dest    = subfolder / f'{name}.plan'

            copied = False

            if force or not problem_dest.exists():
                shutil.copy(src_path / f'{name}.pddl', problem_dest)
                copied = True

            if force or not plan_dest.exists():
                shutil.copy(src_path / f'{name}.plan', plan_dest)
                copied = True

            if copied:
                print(f"   → {name} файлы {'перезаписаны' if force else 'скопированы'}")
            else:
                print(f"   → {name} уже существует (force=False) — пропущено")


def process_domains(domains, force: bool = False):
    """
    Запускает shuffle для всех проблем всех доменов.
    
    force=False (по умолчанию) — безопасный режим:
        • если в папке p01 уже есть canonical/ (т.е. shuffle уже был сделан) — пропускаем
        • force=True — пересоздаём ВСЁ заново (полезно при изменении логики shuffle)
    """
    total_problems = len(domains) * 20
    processed = 0
    skipped = 0

    for d in domains:
        src_path = Path(f'materials/{d}')
        domain_file = src_path / 'domain.pddl'
        
        print(f"\n🔄 Домен: {d}  ({len(domains)}/{len(domains)})")
        
        for i in range(1, 21):
            name = f'p{i:02d}'
            problem_file = src_path / name / f'{name}.pddl'
            optimal_plan_file = src_path / name / f'{name}.plan'
            shuffle_path = src_path / name

            # Проверяем, был ли уже shuffle
            already_shuffled = (shuffle_path / 'canonical').exists()

            if already_shuffled and not force:
                print(f"   ⏭  {name} — уже обработан (canonical/ существует), пропуск")
                skipped += 1
            else:
                if already_shuffled and force:
                    print(f"   ♻️  {name} — force=True, пересоздаём shuffle")
                else:
                    print(f"   ▶️  {name} — генерация 14 вариантов...")
                
                shuffle(domain_file, problem_file, optimal_plan_file, shuffle_path)
                processed += 1

    print(f"\n{'='*80}")
    print(f"✅ process_domains завершён!")
    print(f"   Обработано: {processed} проблем")
    print(f"   Пропущено (уже было): {skipped} проблем")
    print(f"   Всего проблем в датасете: {total_problems}")
    if force:
        print("   ⚠️  Режим force=True — все shuffle пересозданы")

