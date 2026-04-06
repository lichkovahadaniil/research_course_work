from dotenv import load_dotenv
from groq import Groq
import os
import subprocess # like terminal commands in python
import re
import pddlpy
import random

DOMAIN = 'domains/original/blocksworld/domain.pddl'
PROBLEM = 'domains/original/blocksworld/instances/instance-1.pddl'

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
    new_order = []

    for i in range(random_domains):
        random.shuffle(actions)
        new_order.append(actions[:])
    
    return new_order


def shuffle(domain, problem, shuffle_path='domains/shuffle'):
    '''
    Returns domains:
    1 - canonical;
    2 - Random with average;
    3 - Optimal;
    4 - With dispersion;
    5 - group by actions type (using llm)
    6 - sort by frequency of occurrence in the optimal plan
    7 - actions with fewer  preconditions
    '''
    names = ['blocksworld']
    randoms = 10

    with open(domain, 'r', encoding='utf-8') as f:
        domain_text = f.read()

    header, actions_blocks, footer = extract_actions_blocks(domain_text)

    canonical_order_list = actions_list(domain, problem) 
    random_order_list = random_order(domain, problem, randoms)


    action_body = {}

    for i, act in enumerate(canonical_order_list):
        action_body[act] = actions_blocks[i]

    # write cacnonical
    with open(f'{shuffle_path}/{names[0]}/domain_canonical.pddl', 'w', encoding='utf-8') as f:
        f.write(header)
        for i in range(len(canonical_order_list)):
            f.write(action_body[canonical_order_list[i]])

        f.write(footer)
    
    for ind in range(randoms):
        curr_random_list = random_order_list[ind]
        with open(f'{shuffle_path}/{names[0]}/domain_random_{ind}.pddl', 'w', encoding='utf-8') as f:
            f.write(header)
            for i in range(len(curr_random_list)):
                f.write(action_body[curr_random_list[i]])

            f.write(footer)


    return action_body, random_order_list

print(shuffle(DOMAIN, PROBLEM))