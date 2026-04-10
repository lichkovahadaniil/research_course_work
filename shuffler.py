from dotenv import load_dotenv
from checker import run_downward_optimal
from groq import Groq
import os
import subprocess
import re
import pddlpy
import random
from pathlib import Path
from vars import DOMAIN, PROBLEM

random.seed(52)

# ====================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ======================
def actions_list(domain, problem):
    """Только имена действий (pddlpy-proof)"""
    dp = pddlpy.DomainProblem(domain, problem)
    ops = list(dp.operators())
    return [op.name if hasattr(op, 'name') else str(op) for op in ops]


def extract_actions_blocks(domain_text: str):
    """Возвращает (header, action_dict, footer). action_dict = {name: full_block}"""
    action_dict = {}
    i = 0
    n = len(domain_text)

    while i < n:
        if domain_text[i] == ';':
            while i < n and domain_text[i] != '\n':
                i += 1
            if i < n:
                i += 1
            continue

        slice_20 = domain_text[i:i+20].lower()
        is_action = slice_20.startswith('(:action')
        is_durative = slice_20.startswith('(:durative-action')

        if is_action or is_durative:
            start = i
            while start > 0 and domain_text[start - 1] in ' \t\n':
                start -= 1

            depth = 0
            j = i
            while j < n:
                if domain_text[j] == '(':
                    depth += 1
                elif domain_text[j] == ')':
                    depth -= 1
                    if depth == 0:
                        action_block = domain_text[start:j + 1]

                        # извлекаем имя
                        name_match = re.search(r'\(\s*:action\s+([\w-]+)', action_block, re.IGNORECASE)
                        if not name_match:
                            name_match = re.search(r'\(\s*:durative-action\s+([\w-]+)', action_block, re.IGNORECASE)
                        name = name_match.group(1) if name_match else f"unknown_{len(action_dict)}"

                        action_dict[name] = action_block
                        i = j + 1
                        break
                j += 1
            continue
        i += 1

    if not action_dict:
        return domain_text, {}, ''

    first_block = next(iter(action_dict.values()))
    first_pos = domain_text.find(first_block)
    header = domain_text[:first_pos].rstrip()

    last_block = list(action_dict.values())[-1]
    last_pos = domain_text.rfind(last_block) + len(last_block)
    footer = domain_text[last_pos:].lstrip('\n')

    return header, action_dict, footer


def random_order(domain, problem, random_domains: int):
    actions = actions_list(domain, problem)
    new_orders = []
    for _ in range(random_domains):
        shuffled = actions[:]
        random.shuffle(shuffled)
        new_orders.append(shuffled)
    return new_orders


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
    dct = {}
    seen = set()
    for name in action_names:
        if name in canonical_order_list:
            dct[name] = dct.get(name, 0) + 1
            seen.add(name)
    for act in canonical_order_list:
        if act not in seen:
            dct[act] = 0
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
def shuffle(domain, problem, opt_plan, save_dir):

    with open(domain, 'r', encoding='utf-8') as f:
        domain_text = f.read()

    header, action_dict, footer = extract_actions_blocks(domain_text)
    canonical_order_list = actions_list(domain, problem)

    random_order_list = random_order(domain, problem, 10)

    with open(opt_plan, 'r', encoding='utf-8') as f:
        optimal_plan_text = f.read()

    optimal_order_list = get_plan_order(optimal_plan_text, canonical_order_list)
    frequency_order_list = get_frequency_order(optimal_plan_text, canonical_order_list)
    dispersion_order_list, chosen_random_idx = get_dispersion_order_with_source(random_order_list, frequency_order_list)

    def save_domain(shuffle_type: str, order_list):
        path = save_dir / f"domain_{shuffle_type}.pddl"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(header)
            for act in order_list:
                f.write(action_dict[act])
            f.write(footer)

    save_domain('canonical', canonical_order_list)
    save_domain('optimal', optimal_order_list)
    save_domain('frequency', frequency_order_list)
    save_domain('dispersion', dispersion_order_list)
    save_domain('random_dispersion_source', random_order_list[chosen_random_idx])