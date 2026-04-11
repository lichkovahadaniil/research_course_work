import re
import random
from pathlib import Path
import json

random.seed(52)

def get_action_name(action_block: str) -> str | None:
    match = re.search(r'\(\s*:action\s+([^\s)]+)', action_block, re.IGNORECASE)
    return match.group(1) if match else None

def extract_actions_blocks(domain_text: str):
    """
    Возвращает: (header, action_map: dict[name → block], footer, canonical_order_list)
    Полностью сохраняет оригинальное форматирование + whitespace.
    Работает даже с 'define(domainrecharging-robots)' без пробелов.
    """
    action_map = {}
    canonical_order_list = []
    i = 0
    n = len(domain_text)

    while i < n:
        if domain_text[i] == ';':  # пропуск комментариев
            while i < n and domain_text[i] != '\n':
                i += 1
            if i < n:
                i += 1
            continue

        if i + 8 <= n and domain_text[i:i+8].lower() == '(:action':
            start = i
            while start > 0 and domain_text[start - 1] in ' \t\n':
                start -= 1

            depth = 0
            j = i
            while j < n:
                if domain_text[j] == '(': depth += 1
                elif domain_text[j] == ')': 
                    depth -= 1
                    if depth == 0:
                        block = domain_text[start:j + 1]
                        name = get_action_name(block)
                        if name:
                            action_map[name] = block
                            canonical_order_list.append(name)
                        i = j + 1
                        break
                j += 1
            continue
        i += 1

    if not action_map:
        return domain_text, {}, '', []

    # header и footer
    first_block = next(iter(action_map.values()))
    first_pos = domain_text.find(first_block)
    header = domain_text[:first_pos].rstrip()

    last_block = list(action_map.values())[-1]
    last_pos = domain_text.rfind(last_block) + len(last_block)
    footer = domain_text[last_pos:].lstrip('\n')

    return header, action_map, footer, canonical_order_list


def get_plan_order(plan_text: str, canonical_order_list: list) -> list:
    action_names = re.findall(r'\(([\w-]+)', plan_text)
    seen = set()
    plan_order = []
    for name in action_names:
        if name in canonical_order_list and name not in seen:
            seen.add(name)
            plan_order.append(name)
    for act in canonical_order_list:
        if act not in seen:
            plan_order.append(act)
    return plan_order


def get_frequency_order(plan_text: str, canonical_order_list: list) -> list:
    action_names = re.findall(r'\(([\w-]+)', plan_text)
    dct = {act: 0 for act in canonical_order_list}
    for name in action_names:
        if name in dct:
            dct[name] += 1
    return sorted(dct, key=dct.get, reverse=True)


def kendall_tau_dist(order1: list, order2: list) -> int:
    pos = {act: idx for idx, act in enumerate(order2)}
    inversions = 0
    for i in range(len(order1)):
        for j in range(i + 1, len(order1)):
            if pos[order1[i]] > pos[order1[j]]:
                inversions += 1
    return inversions


def get_dispersion_order_with_source(random_orders_list: list, freq_order: list):
    max_dist = -1
    best_order = None
    best_idx = -1
    for idx, candidate in enumerate(random_orders_list):
        dist = kendall_tau_dist(candidate, freq_order)
        if dist > max_dist:
            max_dist = dist
            best_order = candidate[:]
            best_idx = idx
    return best_order, best_idx


# ====================== ОСНОВНАЯ ФУНКЦИЯ ======================
def shuffle(domain_path: str | Path, problem_path: str | Path, 
            optimal_plan_path: str | Path, save_dir: str | Path):
    domain_path = Path(domain_path)
    problem_path = Path(problem_path)
    optimal_plan_path = Path(optimal_plan_path)
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    with open(domain_path, 'r', encoding='utf-8') as f:
        domain_text = f.read()

    header, action_map, footer, canonical_order_list = extract_actions_blocks(domain_text)

    # 10 случайных порядков
    random_order_list = []
    for _ in range(10):
        shuffled = canonical_order_list[:]
        random.shuffle(shuffled)
        random_order_list.append(shuffled)

    with open(optimal_plan_path, 'r', encoding='utf-8') as f:
        optimal_plan_text = f.read()

    optimal_order_list = get_plan_order(optimal_plan_text, canonical_order_list)
    frequency_order_list = get_frequency_order(optimal_plan_text, canonical_order_list)
    dispersion_order_list, chosen_idx = get_dispersion_order_with_source(
        random_order_list, frequency_order_list
    )

    def save_domain(subdir_name: str, order_list: list):
        """Создаёт поддиректорию и кладёт туда domain.pddl"""
        subdir = save_dir / subdir_name
        subdir.mkdir(parents=True, exist_ok=True)
        path = subdir / 'domain.pddl'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(header + '\n')
            for act in order_list:
                f.write(action_map[act])
            f.write(footer)

    # Специальные порядки
    save_domain('canonical', canonical_order_list)
    save_domain('optimal', optimal_order_list)
    save_domain('frequency', frequency_order_list)
    save_domain('dispersion', dispersion_order_list)

    # Все 10 рандомов
    for idx, order in enumerate(random_order_list, start=1):
        save_domain(f'random_{idx:02d}', order)

    print(f"✅ {save_dir.name} → 4 special + 10 random (14 поддиректорий)")

    # Метаданные
    meta = {
        "canonical": canonical_order_list,
        "optimal": optimal_order_list,
        "frequency": frequency_order_list,
        "dispersion": dispersion_order_list,
        "dispersion_from_random_idx": chosen_idx + 1,
        "all_random_orders": random_order_list
    }
    with open(save_dir / "shuffle_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)