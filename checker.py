import subprocess
import re
from pathlib import Path

def validate_plan(domain_path, problem_path, plan_path):
    result = subprocess.run(
        ['validate', domain_path, problem_path, plan_path], 
        capture_output=True, text=True
    )
    output = result.stdout + result.stderr
    return ('Plan valid' in output), output

def get_plan_cost(plan_path):
    with open(plan_path) as f:
        lines = f.readlines()
    actions = [l for l in lines if l.strip() and not l.startswith(';')]
    return len(actions)

def run_downward_optimal(domain_path, problem_path, optimal_plan_path=None):
    """
    Если файл optimal_plan_path уже существует — просто читаем cost из него.
    Если нет — запускаем Fast-Downward и сохраняем.
    """
    if optimal_plan_path is None:
        optimal_plan_path = Path(f"plans/optimal/{Path(domain_path).stem}_{Path(problem_path).stem}.txt")
    else:
        optimal_plan_path = Path(optimal_plan_path)
    
    optimal_plan_path.parent.mkdir(parents=True, exist_ok=True)

    # Если оптимальный план уже есть — просто парсим cost
    if optimal_plan_path.exists():
        with open(optimal_plan_path, encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'Plan cost:\s*(\d+)', content)
        if match:
            cost = int(match.group(1))
            return cost, "Using pre-computed optimal plan", str(optimal_plan_path)

    # Иначе запускаем Fast-Downward
    res = subprocess.run(
        [
            '/Users/daniillickovaha/downward/fast-downward.py',
            '--plan-file', str(optimal_plan_path),
            domain_path,
            problem_path,
            '--search',
            'astar(lmcut())',
        ],
        capture_output=True,
        text=True
    )

    output = res.stdout + res.stderr
    match = re.search(r'Plan cost:\s*(\d+)', output)
    if match:
        cost = int(match.group(1))
        return cost, output, str(optimal_plan_path)
    else:
        return None, output, str(optimal_plan_path)

def compute_gap(llm_cost, optimal_cost):
    if optimal_cost == 0:
        return 0
    return (llm_cost - optimal_cost) / optimal_cost

def plan_downward_metric(domain_path, problem_path, plan_path, optimal_plan_path=None):
    llm_plan_cost = get_plan_cost(plan_path)
    optimal_plan_cost, log, used_path = run_downward_optimal(domain_path, problem_path, optimal_plan_path)

    if optimal_plan_cost is None:
        return {'error': 'Downward didnt find optimal plan', 'log': log}

    gap = compute_gap(llm_plan_cost, optimal_plan_cost)
    return {
        'llm_cost': llm_plan_cost,
        'optimal_cost': optimal_plan_cost,
        'gap': gap,
        'optimal_plan_path': used_path
    }

# Основная функция
def build_metrics(dmain_path, problem_path, plan_path, optimal_plan_path=None):
    return {
        'VAL': validate_plan(dmain_path, problem_path, plan_path),
        'FD': plan_downward_metric(dmain_path, problem_path, plan_path, optimal_plan_path)
    }