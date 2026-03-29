import random
import re
from pathlib import Path
import json

def extract_actions(domain_text: str):
    """Извлекает блоки :action целиком"""
    # Простой regex, хорошо работает для классических доменов
    pattern = r'(\(:action .*?)(?=\n\s*\(:action|\n\s*\(:predicates|\n\s*\(:types|\n\s*\(:requirements|\Z))'
    actions = re.findall(pattern, domain_text, re.DOTALL | re.IGNORECASE)
    return [a.strip() for a in actions]

def reconstruct_domain(domain_text: str, new_actions: list):
    """Заменяет старые :action на новые в нужном порядке"""
    # Удаляем старые action-блоки
    cleaned = re.sub(r'\(:action .*?(?=\n\s*\(:action|\n\s*\(:predicates|\n\s*\(:types|\n\s*\(:requirements|\Z)', '', domain_text, flags=re.DOTALL | re.IGNORECASE)
    # Вставляем новые в конец перед закрывающей скобкой
    new_actions_str = '\n\n'.join(new_actions)
    cleaned = cleaned.rstrip() + '\n\n' + new_actions_str + '\n)'
    return cleaned

def create_shuffled_domain(original_domain_path: str, ordering_type: str, 
                           optimal_action_order: list = None, dispersion_rate: float = 0.0, seed: int = 42):
    random.seed(seed)
    domain_text = Path(original_domain_path).read_text(encoding='utf-8')
    actions = extract_actions(domain_text)
    
    if ordering_type == "canonical":
        new_actions = actions
    elif ordering_type == "alphabetical":
        new_actions = sorted(actions, key=lambda x: re.search(r':action\s+(\w+)', x).group(1))
    elif ordering_type == "reverse":
        new_actions = actions[::-1]
    elif ordering_type == "random":
        new_actions = actions[:]
        random.shuffle(new_actions)
    elif ordering_type == "optimal" and optimal_action_order:
        # Сортируем по оптимальному порядку
        order_dict = {name: idx for idx, name in enumerate(optimal_action_order)}
        def sort_key(act):
            name_match = re.search(r':action\s+(\w+)', act)
            name = name_match.group(1) if name_match else ""
            return order_dict.get(name, 9999)
        new_actions = sorted(actions, key=sort_key)
    elif ordering_type == "dispersion" and optimal_action_order:
        # Сначала optimal, потом добавляем шум
        order_dict = {name: idx for idx, name in enumerate(optimal_action_order)}
        new_actions = sorted(actions, key=lambda x: order_dict.get(re.search(r':action\s+(\w+)', x).group(1) if re.search(r':action\s+(\w+)', x) else "", 9999))
        # Дисперсия: случайные свапы
        for _ in range(int(len(new_actions) * dispersion_rate)):
            if len(new_actions) > 1:
                i, j = random.sample(range(len(new_actions)), 2)
                new_actions[i], new_actions[j] = new_actions[j], new_actions[i]
    else:
        new_actions = actions
    
    new_domain = reconstruct_domain(domain_text, new_actions)
    return new_domain

# Пример использования
if __name__ == "__main__":
    # Сначала получи optimal_action_order из API (см. ниже)
    optimal_order = ["unstack", "put-down", "pick-up", "stack"]  # пример для Blocksworld
    new_dom = create_shuffled_domain("domains/original/blocksworld/domain.pddl", "optimal", optimal_order)
    Path("shuffled/blocksworld_optimal.pddl").write_text(new_dom)