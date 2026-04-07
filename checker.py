import subprocess # like terminal commands in python
import re
from pathlib import Path

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

def run_downward_optimal(domain_path, problem_path, optimal_plan_path=None):

    if optimal_plan_path is None:
        optimal_plan_path = f"plans/plan_optimal_{Path(domain_path).stem}_{Path(problem_path).stem}.txt"

    res = subprocess.run(
        [
            '/Users/daniillickovaha/downward/fast-downward.py',
            '--plan-file', optimal_plan_path, # save optimal plan in file
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
        return cost, output, optimal_plan_path
    else:
        return None, output, optimal_plan_path

def compute_gap(llm_cost, optimal_cost):
    if optimal_cost == 0:
        return 0
    return (llm_cost - optimal_cost) / optimal_cost

def plan_downward_metric(domain_path, problem_path, plan_path):
    llm_plan_cost = get_plan_cost(plan_path)
    optimal_plan_cost, log, OPTIMAL_PLAN = run_downward_optimal(domain_path, problem_path)

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


# main function
def build_metrics(dmain_path, problem_path, plan_path):
    return {
        'VAL': validate_plan(dmain_path, problem_path, plan_path),
        'FD': plan_downward_metric(dmain_path, problem_path, plan_path)
    }