from dotenv import load_dotenv
from groq import Groq
import os
import re
from shuffler import *
from checker import *
from vars import *

load_dotenv()

def call(domain=DOMAIN, problem=PROBLEM, plan_path=PLAN):
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))

    def read_pddl(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
        
    domain_text = read_pddl(domain)
    problem_text = read_pddl(problem)

    prompt = f"""
You are an expert PDDL planner. Generate ONLY a valid plan.
No explanations, no comments, no markdown, no extra text.

Domain:
{domain_text}

Problem:
{problem_text}

Return ONLY the plan — one action per line:
(pick-up b)
(stack b a)
...
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # ← оставляем, она лучше всего работает
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.0,
        max_tokens=2048,
    )

    raw = response.choices[0].message.content.strip()

    # === СУПЕР-РОБАСТНАЯ ОЧИСТКА ===
    lines = raw.splitlines()
    cleaned = []
    for line in lines:
        line = line.strip()
        if line.startswith('(') and line.endswith(')') and len(line) > 5:
            cleaned.append(line)

    # Если ничего не поймали — пробуем жёсткий regex (ловит даже если есть текст вокруг)
    if not cleaned:
        cleaned = re.findall(r'\([^(]+?\)', raw)

    final_plan = "\n".join(cleaned)

    if not final_plan:
        print(f"⚠️  EMPTY PLAN AFTER CLEANING! Raw preview: {raw[:300]}...")
        final_plan = "; LLM returned empty plan"

    with open(plan_path, "w", encoding='utf-8') as f:
        f.write(final_plan)

    print(f"      ✓ Plan saved to {plan_path} ({len(cleaned)} actions)")
    return final_plan