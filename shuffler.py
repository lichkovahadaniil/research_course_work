from dotenv import load_dotenv
from checker import run_downward_optimal
from groq import Groq
import os
import subprocess # like terminal commands in python
import re
import pddlpy
import random
from vars import DOMAIN, PROBLEM

random.seed(52)

def actions_list(domain, problem):
    dp = pddlpy.DomainProblem(domain, problem)
    return list(dp.operators()) # list of actions

def extract_actions_blocks(domain_text: str):
    """
    Возвращает: (header, list_of_action_blocks, footer)
    Гарантирует побайтовое совпадение с оригиналом при записи canonical.
    """
    action_blocks = []
    i = 0
    n = len(domain_text)

    while i < n:
        # Пропускаем комментарии (если будут)
        if domain_text[i] == ';':
            start = i
            while i < n and domain_text[i] != '\n':
                i += 1
            if i < n:
                i += 1
            continue

        # Нашли начало действия
        if i + 8 <= n and domain_text[i:i+8].lower() == '(:action':
            # Захватываем ВЕСЬ leading whitespace перед (:action
            start = i
            while start > 0 and domain_text[start - 1] in ' \t\n':
                start -= 1

            # Парсим action до баланса скобок
            depth = 0
            j = i
            while j < n:
                if domain_text[j] == '(':
                    depth += 1
                elif domain_text[j] == ')':
                    depth -= 1
                    if depth == 0:
                        action_block = domain_text[start:j + 1]
                        action_blocks.append(action_block)
                        i = j + 1
                        break
                j += 1
            continue

        i += 1

    # === Теперь точно вырезаем header и footer из оригинального текста ===
    if not action_blocks:
        return domain_text, [], ''

    # Header — всё до первого action (включая его leading whitespace — он уже в action_blocks[0])
    first_action_text = action_blocks[0]
    first_pos = domain_text.find(first_action_text)
    header = domain_text[:first_pos].rstrip()

    # Footer — всё после ПОСЛЕДНЕГО action
    last_action_text = action_blocks[-1]
    last_pos = domain_text.rfind(last_action_text) + len(last_action_text)
    footer = domain_text[last_pos:].lstrip('\n')

    return header, action_blocks, footer


random.seed(52)
def random_order(domain, problem, random_domains: int):
    f'''generate {random_domains} random orders in transferred domain'''
    actions = actions_list(domain, problem) # canonical
    new_orders = []

    for i in range(random_domains):
        random.shuffle(actions)
        new_orders.append(actions[:])
    
    return new_orders

def get_plan_order(plan_text: str, canonical_order_list: list) -> list:
    """
    Извлекает порядок действий в той последовательности,
    в которой они впервые появляются в оптимальном плане.
    Возвращает список имён действий в порядке первого появления.
    """
    # Извлекаем все имена действий из плана
    action_names = re.findall(r'\(([\w-]+)', plan_text)
    
    # Оставляем только те, которые есть в домене
    seen = set()
    plan_order = []
    
    for name in action_names:
        if name in canonical_order_list and name not in seen:
            seen.add(name)
            plan_order.append(name)
            # print(name)
    
    # Если в плане использованы не все действия — добавляем оставшиеся
    # в конец в оригинальном canonical порядке (stable)
    for act in canonical_order_list:
        if act not in seen:
            plan_order.append(act)
    
    return plan_order

def get_frequency_order(plan_text: str, canonical_order_list: list) -> list:
    """
    Считает, сколько раз каждое действие встретилось в оптимальном плане.
    Возвращает список имён действий по их "популярности" в оптимальном плане.
    """
    # Извлекаем все имена действий из плана
    action_names = re.findall(r'\(([\w-]+)', plan_text)
    
    dct = {}
    seen = set()
    
    for name in action_names:
        if name in canonical_order_list:
            dct[name] = 1 if name not in dct else 1 + dct[name]
            seen.add(name)
    
    # Если в плане использованы не все действия — добавляем оставшиеся
    # в конец в оригинальном canonical порядке (stable)
    for act in canonical_order_list:
        if act not in seen:
            dct[act] = 0
    
    res = sorted(dct, key=dct.get)[::-1]
    return res

# variance with respect to permutations (inversions)
def kendall_tau_dist(order1: list, order2: list) -> int:
    '''kendall-tau distance (numbers of inversions) the larger, the strongest the variance'''
    pos = {act: idx for idx, act in enumerate(order2)}
    inversions = 0
    for i in range(len(order1)):
        for j in range(i + 1, len(order1)):
            if pos[order1[i]] > pos[order1[j]]: # 5 4 -> 4 5
                inversions += 1
    return inversions

def get_dispersion_order(random_orders_list: list, freq_order: list) -> list:
    """
    Из 10 случайных перестановок выбирает ту, которая максимально
    отличается (по Kendall-tau) от frequency-упорядоченного списка.
    """
    max_dist = -1
    best_order = None

    for candidate in random_orders_list:
        dist = kendall_tau_dist(candidate, freq_order)
        if dist > max_dist:
            max_dist = dist
            best_order = candidate[:]

    return best_order

def get_dispersion_order_with_source(random_orders_list: list, freq_order: list):
    """
    Возвращает (dispersion_order, chosen_random_index)
    """
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

def shuffle(domain, problem, domain_name: str, instance_name: str, shuffle_path='domains/shuffle'):
    """
    Phase 1 only: генерирует домены БЕЗ вызова LLM.
    Сохраняет выбранный random, который стал dispersion.
    """
    base_path = f'{shuffle_path}/{domain_name}'
    os.makedirs(base_path, exist_ok=True)

    with open(domain, 'r', encoding='utf-8') as f:
        domain_text = f.read()

    header, actions_blocks, footer = extract_actions_blocks(domain_text)

    canonical_order_list = actions_list(domain, problem)
    random_order_list = random_order(domain, problem, 10)   # только в памяти

    # instance-specific optimal plan
    cost, output, OPTIMAL_PLAN = run_downward_optimal(domain, problem)
    with open(OPTIMAL_PLAN, 'r', encoding='utf-8') as f:
        optimal_plan_text = f.read()

    optimal_order_list = get_plan_order(optimal_plan_text, canonical_order_list)
    frequency_order_list = get_frequency_order(optimal_plan_text, canonical_order_list)
    dispersion_order_list, chosen_random_idx = get_dispersion_order_with_source(random_order_list, frequency_order_list)

    action_body = {act: actions_blocks[i] for i, act in enumerate(canonical_order_list)}

    def save_domain(filename, order_list):
        path = f'{base_path}/{filename}'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(header)
            for act in order_list:
                f.write(action_body[act])
            f.write(footer)

    save_domain(f'domain_canonical_{instance_name}.pddl', canonical_order_list)
    save_domain(f'domain_optimal_{instance_name}.pddl', optimal_order_list)
    save_domain(f'domain_frequency_{instance_name}.pddl', frequency_order_list)
    save_domain(f'domain_dispersion_{instance_name}.pddl', dispersion_order_list)
    
    # ← Новый файл: тот самый random, который стал dispersion
    save_domain(f'domain_random_dispersion_source_{instance_name}.pddl', random_order_list[chosen_random_idx])

    print(f"   ✅ 5 instance-specific domains generated for {domain_name}/{instance_name} "
          f"(including dispersion source random #{chosen_random_idx})")
    return

# print(shuffle(DOMAIN, PROBLEM))

# a = {'a': 2, 'b': 3, 'c': 1}
# print(a.get, sorted(a, key=a.get)[::-1], sorted(a, key=lambda x: a[x])[::-1])