from groq import Groq
from pathlib import Path
import os
from domain_shuffler import create_shuffled_domain
from api_client import call_solve, call_validate, extract_action_order_from_plan

from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def read_file(p): return Path(p).read_text(encoding='utf-8')

# === 1. Получаем Optimal порядок действий ===
domain_orig = read_file("domains/original/blocksworld/domain.pddl")
problem = read_file("domains/original/blocksworld/instances/instance-1.pddl")

solve_result = call_solve(domain_orig, problem)
print("Solve status:", solve_result.get("status"))

optimal_action_order = extract_action_order_from_plan(solve_result)
print("Optimal action order для этой проблемы:", optimal_action_order)

# === 2. Генерируем разные ordering'ы ===
ordering_types = ["canonical", "alphabetical", "reverse", "random", "optimal", "dispersion"]

for ord_type in ordering_types:
    disp_rate = 0.3 if ord_type == "dispersion" else 0.0
    shuffled_domain_text = create_shuffled_domain(
        "domains/original/blocksworld/domain.pddl",
        ord_type,
        optimal_action_order,
        dispersion_rate=disp_rate,
        seed=42
    )
    
    Path(f"shuffled/blocksworld_{ord_type}.pddl").write_text(shuffled_domain_text)
    
    # === 3. Генерируем план через Groq ===
    system = "Ты эксперт по PDDL. Сгенерируй только план в формате IPC (одно действие на строку в скобках)."
    user = f"Domain:\n{shuffled_domain_text}\n\nProblem:\n{problem}\n\nПлан:"
    
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"system", "content":system}, {"role":"user", "content":user}],
        temperature=0.0,
        max_tokens=800,
        seed=42
    )
    plan = resp.choices[0].message.content
    Path(f"plans/llm_plan_{ord_type}.plan").write_text(plan)
    
    # === 4. Оцениваем через API ===
    val_result = call_validate(shuffled_domain_text, problem, plan)
    print(f"\n=== {ord_type.upper()} ===")
    print("VAL status:", val_result.get("val_status"))
    print("VAL stdout:", val_result.get("val_stdout", "")[:300])
    
    # Оптимальная длина (из предыдущего solve)
    opt_length = solve_result.get("length", 0)
    llm_length = len([line for line in plan.splitlines() if line.strip().startswith("(")])
    gap = (llm_length - opt_length) / opt_length if opt_length > 0 else 0
    print(f"Plan length: {llm_length}, Optimal: {opt_length}, Gap: {gap:.3f}")