import subprocess
import re
from pathlib import Path
from typing import List, Tuple, Dict

def validate_plan(domain_path, problem_path, plan_path):
    result = subprocess.run(
        ['validate', domain_path, problem_path, plan_path], 
        capture_output=True, text=True
    )
    output = result.stdout + result.stderr
    is_valid = 'Plan valid' in output
    return is_valid, output


def extract_plan_cost_from_validate(output: str) -> float | None:
    """Извлекает реальную стоимость из вывода validate"""
    # 1. Классический вариант
    match = re.search(r'Plan cost:\s*(\d+\.?\d*)', output)
    if match:
        return float(match.group(1))
    
    # 2. Folding / новые домены (самое важное!)
    match = re.search(r'Final value:\s*(\d+\.?\d*)', output)
    if match:
        return float(match.group(1))
    
    return None


def get_actions_sequence(plan_path: str | Path) -> List[str]:
    """Извлекает только имена действий в порядке выполнения"""
    with open(plan_path, encoding='utf-8') as f:
        lines = f.readlines()
    
    actions = []
    for line in lines:
        line = line.strip()
        if line.startswith('(') and line.endswith(')'):
            # берём первое слово внутри скобок
            match = re.match(r'\(([\w-]+)', line)
            if match:
                actions.append(match.group(1))
    return actions


def action_order_distance(llm_plan_path: str | Path, optimal_plan_path: str | Path) -> Dict:
    """
    Комбинированная метрика:
    - Kendall-Tau на общих действиях
    - +1 за каждое лишнее действие (insertion)
    - +1 за каждое пропущенное действие (deletion)
    """
    llm_seq = get_actions_sequence(llm_plan_path)
    opt_seq = get_actions_sequence(optimal_plan_path)

    # Общие действия (сохраняем порядок в оптимальном)
    common = [a for a in opt_seq if a in llm_seq]

    # Kendall-Tau только на общих действиях
    def kendall_tau(order1: List[str], order2: List[str]) -> int:
        pos = {act: idx for idx, act in enumerate(order2)}
        inversions = 0
        for i in range(len(order1)):
            for j in range(i + 1, len(order1)):
                if pos.get(order1[i], -1) > pos.get(order1[j], -1):
                    inversions += 1
        return inversions

    if len(common) >= 2:
        tau = kendall_tau([a for a in llm_seq if a in common], common)
    else:
        tau = 0

    # Штрафы за insertions и deletions
    insertions = len(llm_seq) - len(common)   # лишние действия
    deletions = len(opt_seq) - len(common)    # пропущенные действия

    total_distance = tau + insertions + deletions

    # Нормализация (примерно от 0 до 1)
    max_possible = len(opt_seq) * (len(opt_seq) - 1) // 2 + len(opt_seq)  # худший случай
    normalized = total_distance / max_possible if max_possible > 0 else 0

    return {
        'kendall_tau_inversions': tau,
        'insertions': insertions,
        'deletions': deletions,
        'total_distance': total_distance,
        'normalized_distance': round(normalized, 4),
        'llm_actions_count': len(llm_seq),
        'optimal_actions_count': len(opt_seq)
    }


def build_metrics(domain_path, problem_path, plan_path, optimal_plan_path=None):
    # 1. Валидация + РЕАЛЬНАЯ стоимость LLM-плана
    is_valid, val_output = validate_plan(domain_path, problem_path, plan_path)
    llm_cost = extract_plan_cost_from_validate(val_output)

    # Fallback: если validate ничего не дал — используем длину (на всякий случай)
    llm_actions_len = len(get_actions_sequence(plan_path))
    if llm_cost is None:
        llm_cost = llm_actions_len

    # 2. РЕАЛЬНАЯ оптимальная стоимость
    optimal_cost = None
    optimal_actions_len = None
    if optimal_plan_path and optimal_plan_path.exists():
        with open(optimal_plan_path, encoding='utf-8') as f:
            content = f.read()
        
        # Пробуем разные варианты комментариев
        match = re.search(r'Plan cost:\s*(\d+\.?\d*)', content)
        if not match:
            match = re.search(r'Optimal cost:\s*(\d+\.?\d*)', content, re.IGNORECASE)
        
        if match:
            optimal_cost = float(match.group(1))
        else:
            optimal_cost = len(get_actions_sequence(optimal_plan_path))
        
        optimal_actions_len = len(get_actions_sequence(optimal_plan_path))

    gap = None
    if llm_cost is not None and optimal_cost is not None and optimal_cost != 0:
        gap = (llm_cost - optimal_cost) / optimal_cost

    # 3. Метрика порядка
    order_metric = None
    if optimal_plan_path and optimal_plan_path.exists():
        order_metric = action_order_distance(plan_path, optimal_plan_path)

    return {
        'VAL': (is_valid, val_output),
        'LLM_COST': {
            'cost': llm_cost,           # ← НАСТОЯЩАЯ СТОИМОСТЬ
            'num_actions': llm_actions_len   # ← ДЛИНА ПЛАНА
        },
        'OPTIMAL_COST': optimal_cost,
        'OPTIMAL_ACTIONS_LEN': optimal_actions_len,
        'GAP': gap,
        'ORDER_METRIC': order_metric
    }

# Вспомогательная (оставил для совместимости)
def get_plan_cost(plan_path):
    return len(get_actions_sequence(plan_path))