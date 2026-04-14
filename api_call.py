from openai import OpenAI
import os
import re
from dotenv import load_dotenv

load_dotenv()

def call_openrouter(domain, problem, reasoning_enabled: bool = False):
    """Вызывает модель с/без reasoning. Возвращает чистый dict."""
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv('OPENROUTER_API_KEY'),
    )

    def read_pddl(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    domain_text = read_pddl(domain)
    problem_text = read_pddl(problem)

    prompt = f"""You are an expert PDDL planner. Generate ONLY a valid optimal plan.
No explanations, no comments, no markdown, no extra text.

Domain:
{domain_text}

Problem:
{problem_text}

Return ONLY the plan — one action per line:
(rotate n1 clockwise up right)
...
"""

    response = client.chat.completions.create(
        model="openai/gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        # extra_body={"reasoning": {"enabled": reasoning_enabled}}, # if 5 mini
        extra_body={},
        temperature=0.0,
    )

    msg = response.choices[0].message
    raw_content = msg.content.strip() if msg.content else ""
    final_plan = msg.content

    # # Очистка плана
    # lines = raw_content.splitlines()
    # cleaned = [line.strip() for line in lines 
    #            if line.strip().startswith('(') and line.strip().endswith(')')]

    # if not cleaned:
    #     cleaned = re.findall(r'\([^(]+?\)', raw_content)

    # final_plan = "\n".join(cleaned) or "; LLM returned empty plan"

    # Reasoning (только если был включён)
    reasoning_text = ""
    if reasoning_enabled:
        reasoning_text = msg.reasoning or ""
        if not reasoning_text and hasattr(msg, 'reasoning_details'):
            reasoning_text = "\n".join(
                d.get('text', '') for d in msg.reasoning_details if isinstance(d, dict)
            )

    return {
        "plan": final_plan,
        "reasoning": reasoning_text,
        "reasoning_enabled": reasoning_enabled,
        "model": response.model,
        "prompt_tokens": getattr(response.usage, 'prompt_tokens', None),
        "completion_tokens": getattr(response.usage, 'completion_tokens', None),
        "total_tokens": getattr(response.usage, 'total_tokens', None),
        "raw_preview": raw_content[:500] + "..." if len(raw_content) > 500 else raw_content,
    }