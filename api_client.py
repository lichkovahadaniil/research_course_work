import requests
import json
from pathlib import Path

BASE_URL = "https://solver.planning.domains"

def call_solve(domain_text: str, problem_text: str, planner: str = "fast-downward"):
    """Получаем optimal plan через FD"""
    payload = {
        "domain": domain_text,
        "problem": problem_text,
        "planner": planner   # или "seq-opt-lmcut", "astar", etc.
    }
    response = requests.post(f"{BASE_URL}/solve", json=payload, timeout=60)
    return response.json()

def call_validate(domain_text: str, problem_text: str, plan_text: str):
    """Валидация плана через VAL"""
    payload = {
        "domain": domain_text,
        "problem": problem_text,
        "plan": plan_text
    }
    response = requests.post(f"{BASE_URL}/validate", json=payload, timeout=30)
    return response.json()

def extract_action_order_from_plan(plan_data):
    """Извлекаем последовательность действий из optimal плана"""
    if isinstance(plan_data.get("plan"), list):
        actions = []
        for step in plan_data["plan"]:
            if isinstance(step, dict) and "name" in step:
                # Извлекаем имя действия: (pick-up b1) → pick-up
                name = step["name"].strip("() ").split()[0]
                if name not in actions:
                    actions.append(name)
            elif isinstance(step, str):
                name = step.strip("() ").split()[0]
                if name not in actions:
                    actions.append(name)
        return actions
    return []