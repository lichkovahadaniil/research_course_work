from pathlib import Path
import json

from domain_generation import *   # generate_paths, process_domains, DOMAIN_TYPES
from api_call import *            # call_openrouter + всё, что там есть


if __name__ == '__main__':
    print("Запуск полного пайплайна: генерация доменов + LLM-планирование")

    # 1. Создаём/обновляем базовую структуру (безопасно)
    generate_paths(DOMAIN_TYPES)      # force=False по умолчанию
    process_domains(DOMAIN_TYPES)     # force=False — пропустит уже готовое

    # 2. Запускаем LLM-агента по всем вариантам
    total = len(DOMAIN_TYPES) * 20 * 14
    done = 0

    for d in DOMAIN_TYPES:
        src_path = Path(f'materials/{d}')

        for i in range(1, 21):
            name = f'p{i:02d}'
            curr_path = src_path / name
            problem = curr_path / f'{name}.pddl'

            # Все 14 вариантов доменов
            variants = ['canonical', 'dispersion', 'frequency', 'optimal'] + \
                       [f'random_{j:02d}' for j in range(1, 11)]

            for variant in variants:
                domain_dir = curr_path / variant
                domain = domain_dir / 'domain.pddl'
                plan_path = domain_dir / 'llm_plan.pddl'

                done += 1
                print(f"   [{done:4d}/{total}] {variant:>12} | {name} → ", end="")

                try:
                    res = call_openrouter(domain, problem)

                    # Поддерживаем два возможных возвращаемых типа:
                    if isinstance(res, dict):
                        plan_text = res.get('plan', res.get('output', ''))
                        meta = {k: v for k, v in res.items() if k != 'plan'}
                    else:
                        plan_text = str(res)
                        meta = {}

                    # Сохраняем план
                    with open(plan_path, 'w', encoding='utf-8') as f:
                        f.write(plan_text)

                    # Дополнительно сохраняем метаданные (tokens, cost, time и т.д.)
                    meta_path = domain_dir / 'llm_meta.json'
                    meta['problem'] = str(problem)
                    meta['domain_variant'] = variant
                    with open(meta_path, 'w', encoding='utf-8') as f:
                        json.dump(meta, f, ensure_ascii=False, indent=2)

                    print("✅ сохранён")

                except Exception as e:
                    print(f"❌ ОШИБКА: {e}")
                    # Сохраняем хотя бы ошибку, чтобы потом можно было отдебажить
                    error_path = domain_dir / 'llm_error.txt'
                    with open(error_path, 'w', encoding='utf-8') as f:
                        f.write(f"ERROR: {str(e)}\n")
                    continue

    print("ПАЙПЛАЙН ЗАВЕРШЁН!")
    print(f"   Обработано доменов: {len(DOMAIN_TYPES)} × 20 × 14 = {total}")
    print(f"   Планы сохранены в: materials/<domain>/pXX/<variant>/llm_plan.pddl")
    print("   Метаданные: llm_meta.json рядом с каждым планом")