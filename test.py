import shutil
from pathlib import Path
from shuffler import shuffle

# Список доменов
DOMAIN_TYPES = ['folding', 'labyrinth', 'recharging-robots', 'ricochet-robots', 'rubiks-cube']

def generate_paths(domains):
    # Проходим по каждому домену
    for d in domains:
        # Путь к исходной папке и новой папке
        src_path = Path(f'ipc2023-dataset-main/opt/{d}')
        dest_path = Path(f'materials/{d}')

        # Создаем новую папку, если её еще нет
        dest_path.mkdir(parents=True, exist_ok=True)

        # Копируем файл domain.pddl в новую папку
        shutil.copy(src_path / 'domain.pddl', dest_path)

        # Создаем подпапки p01...p20
        for i in range(1, 21):
            subfolder = dest_path / f'p{i:02d}'
            subfolder.mkdir(exist_ok=True)  # Создаем папку, если её нет

            # Копируем p01.pddl, p01.plan ... p20.pddl, p20.plan
            shutil.copy(src_path / f'p{i:02d}.pddl', subfolder)
            shutil.copy(src_path / f'p{i:02d}.plan', subfolder)


def process_domains(DOMAIN_TYPES):
    for d in DOMAIN_TYPES:
        src_path = Path(f'materials/{d}')
        domain_file = src_path / 'domain.pddl'
        
        for i in range(1, 21):
            name = f'p{i:02d}'
            problem_file = src_path / name / f'p{i:02d}.pddl'
            optimal_plan_file = src_path / name / f'p{i:02d}.plan'
            shuffle_path = src_path / name

            # Генерация перемешанных доменов и планов для каждого p01...p20
            shuffle(domain_file, problem_file, optimal_plan_file, shuffle_path)


# # Запуск обработки всех доменов
# process_domains(DOMAIN_TYPES)

