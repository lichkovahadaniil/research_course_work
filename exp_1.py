from dotenv import load_dotenv
from groq import Groq
import os
import subprocess # like terminal commands in python
import re
import pddlpy
import random

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

DOMAIN = 'domains/original/blocksworld/domain.pddl'
PROBLEM = 'domains/original/blocksworld/instances/instance-1.pddl'

def read_pddl(path):
    with open(path, 'r') as f:
        return f.read()
    
domain_text = read_pddl(DOMAIN)
problem_text = read_pddl(PROBLEM)

prompt = f"""
You are an expert in PDDL planning.

Given the following domain and problem, generate only a valid plan.

Domain:
{domain_text}

Problem:
{problem_text}

Format example:
(move a b c)
(stack a b)
...

Return ONLY the plan as a sequence of actions, one per line.
"""

response = client.chat.completions.create(
    model='openai/gpt-oss-20b',
    messages = [
        {'role': 'user', 'content': prompt}
    ],
    temperature=0,
)

plan = response.choices[0].message.content
# print(response)

def cleaning(plan):
    actions = re.findall(r"\(.*?\)", plan)
    return "\n".join(actions)

plan = cleaning(plan)
plan_path = 'plans/plan_1.txt'
print(plan)

with open(plan_path, "w") as f:
    f.write(plan)


def validate_plan(domain_path, problem_path, plan_path):
    result = subprocess.run(
        ['validate', domain_path, problem_path, plan_path], capture_output=True, text=True
    )

    output = result.stdout + result.stderr

    if 'Plan valid' in output:
        return True, output
    else:
        return False, output
    
def get_plan_cost(plan_path):
    with open(plan_path) as f:
        lines = f.readlines()
    
    # cleaning
    actions = [l for l in lines if l.strip() and not l.startswith(';')] # if l.strip() is True (non empty)
    return len(actions)

def run_downward_optimal(domain_path, problem_path):
    res = subprocess.run(
        [
            '/Users/daniillickovaha/downward/fast-downward.py',
            '--plan-file', 'plans/plan_1_optimal.txt',
            domain_path,
            problem_path,
            '--search', # flag, after that begin a configuration of the planer 'brain'
            'astar(lmcut())', # astar algorithm for optimal plan; landmard-cut for calculate min numbers of rest moves
        ],
        capture_output = True,
        text = True
    )
    output = res.stdout + res.stderr

    # r - row string
    # \s - space or tab
    # * - 0 or more symbols
    # \d - any digit
    # + - one or more digits
    # () - closed group
    match = re.search(r'Plan cost:\s*(\d+)', output)
    if match:
        cost = int(match.group(1)) # group(0) - full match, group(1) - into first ()
        return cost, output
    else:
        return None, output

def compute_gap(llm_cost, optimal_cost):
    if optimal_cost == 0:
        return 0
    return (llm_cost - optimal_cost) / optimal_cost

def plan_downward_metric(domain_path, problem_path, plan_path):
    llm_plan_cost = get_plan_cost(plan_path)
    optimal_plan_cost, log = run_downward_optimal(domain_path, problem_path)

    if optimal_plan_cost is None:
        return {
            'error': 'Downward didnt find optimal plan',
            'log': log
        }

    gap = compute_gap(llm_plan_cost, optimal_plan_cost)
    return {
        'llm_cost': llm_plan_cost,
        'optimal_cost' : optimal_plan_cost,
        'gap': gap
    }


def build_metrics(dmain_path, problem_path, plan_path):
    return {
        'VAL': validate_plan(dmain_path, problem_path, plan_path),
        'FD': plan_downward_metric(dmain_path, problem_path, plan_path)
    }




def actions_list(domain, problem):
    dp = pddlpy.DomainProblem(domain, problem)
    return list(dp.operators()) # list of actions

def extract_actions_blocks(text):
    """
    returns:
    header, actions (list), footer
    consider comments and empty lines
    """
    actions = []
    header = []
    footer = []

    i = 0
    n = len(text)

    in_comment = False
    found_first_action = False

    while i < n:
        # Обработка комментариев
        if text[i] == ';':
            in_comment = True

        if in_comment:
            if not found_first_action:
                header.append(text[i])
            else:
                footer.append(text[i])

            if text[i] == '\n':
                in_comment = False

            i += 1
            continue

        # Обработка действий
        if text[i:i+8] == "(:action":
            found_first_action = True

            start = i
            depth = 0

            while i < n:
                if text[i] == ';':  # комментарий внутри action
                    while i < n and text[i] != '\n':
                        i += 1
                    continue

                if text[i] == '(':
                    depth += 1
                elif text[i] == ')':
                    depth -= 1

                i += 1

                if depth == 0:
                    actions.append(text[start:i])
                    break

            continue

        # --- обычный текст (не комментарий и не действие) ---
        if not found_first_action:
            # Добавляем в header
            if text[i] != '\n' and not (text[i] == ' ' and text[i-1] == ' '):  # Пропуск лишних пробелов
                header.append(text[i])
        else:
            # Добавляем в footer
            if text[i] != '\n' and not (text[i] == ' ' and text[i-1] == ' '):  # Пропуск лишних пробелов
                footer.append(text[i])

        i += 1

    return "".join(header), actions, "".join(footer)


random.seed(52)
def random_order(domain, problem, random_domains: int):
    f'''generate {random_domains} random orders in transferred domain'''
    actions = actions_list(domain, problem) # canonical
    new_order = []

    for i in range(random_domains):
        random.shuffle(actions)
        new_order.append(actions)
    
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

    actions = actions_list(domain, problem) 
    random_order = random_order(domain, problem)







print(build_metrics(DOMAIN, PROBLEM, plan_path), actions_list(DOMAIN, PROBLEM))