from openai import OpenAI
import os
import time
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Кэш поддержки reasoning
CAPABILITIES_CACHE = {}
CACHE_FILE = Path("model_capabilities.json")


def load_cache():
    global CAPABILITIES_CACHE
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, encoding='utf-8') as f:
                CAPABILITIES_CACHE = json.load(f)
        except:
            pass


def save_cache():
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(CAPABILITIES_CACHE, f, ensure_ascii=False, indent=2)


def supports_reasoning(model: str) -> bool:
    if model in CAPABILITIES_CACHE:
        return CAPABILITIES_CACHE[model]

    print(f"   🔍 Проверяем reasoning для {model}... ", end="", flush=True)
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv('OPENROUTER_API_KEY'))

    try:
        client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say OK"}],
            extra_body={"reasoning": {"enabled": True}},
            max_tokens=5,
        )
        CAPABILITIES_CACHE[model] = True
        print("✅ поддерживает")
    except:
        CAPABILITIES_CACHE[model] = False
        print("❌ не поддерживает")
    save_cache()
    return CAPABILITIES_CACHE[model]


def call_openrouter(domain, problem, model: str = "openai/gpt-5-mini", reasoning_enabled: bool = False):
    load_cache()

    # Если модель не поддерживает reasoning — выключаем
    if reasoning_enabled and not supports_reasoning(model):
        reasoning_enabled = False
        print(f"   ⚠️ reasoning отключён (модель не поддерживает)")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv('OPENROUTER_API_KEY'),
        timeout=300.0,
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

    start = time.time()
    mode = "reasoning" if reasoning_enabled else "plain"
    print(f"   → {model} | {mode} ... ", end="", flush=True)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            extra_body={"reasoning": {"enabled": reasoning_enabled}} if reasoning_enabled else {},
            temperature=0.0,
            max_tokens=20000,
        )

        duration = time.time() - start
        print(f"готово ({duration:.1f}s)")

        msg = response.choices[0].message
        raw_content = msg.content.strip() if msg.content else ""

        # Твой оригинальный простой стиль
        final_plan = raw_content

        # Reasoning
        reasoning_text = ""
        if reasoning_enabled:
            reasoning_text = getattr(msg, 'reasoning', '') or ""
            if not reasoning_text and hasattr(msg, 'reasoning_details'):
                reasoning_text = "\n".join(
                    d.get('text', '') for d in msg.reasoning_details if isinstance(d, dict)
                )

        return {
            "plan": final_plan,
            "reasoning": reasoning_text,
            "reasoning_enabled": reasoning_enabled,
            "model": model,
            "duration_sec": round(duration, 2),
            "prompt_tokens": getattr(response.usage, 'prompt_tokens', None),
            "completion_tokens": getattr(response.usage, 'completion_tokens', None),
            "total_tokens": getattr(response.usage, 'total_tokens', None),
        }

    except Exception as e:
        print(f"❌ ОШИБКА ({time.time()-start:.1f}s): {e}")
        raise