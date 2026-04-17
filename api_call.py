from openai import OpenAI
import os
import time
import json
from pathlib import Path
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

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


KNOWN_REASONING_SUPPORT = {
    "openai/gpt-5-mini": True,
    "x-ai/grok-4.1-fast": True,
    "deepseek/deepseek-v3.2": True,
    # "google/gemma-4-31b-it": True,
    "xiaomi/mimo-v2-flash": True,
    "qwen/qwen3.5-35b-a3b:alibaba": True,   # ← НОВАЯ + alibaba
}


def fix_plan_format(plan_text: str) -> str:
    """Исправляет планы без скобок — самая частая проблема open-source моделей"""
    if not plan_text:
        return plan_text
    lines = plan_text.strip().split('\n')
    fixed = []
    for line in lines:
        line = line.strip()
        if line and not (line.startswith('(') and line.endswith(')')):
            # Добавляем скобки, если их нет
            fixed.append(f"({line})")
        else:
            fixed.append(line)
    return '\n'.join(fixed)

def supports_reasoning(model: str) -> bool:
    if model in CAPABILITIES_CACHE:
        return CAPABILITIES_CACHE[model]

    if model in KNOWN_REASONING_SUPPORT:
        CAPABILITIES_CACHE[model] = KNOWN_REASONING_SUPPORT[model]
        save_cache()
        print(f"   🔍 {model} — hardcoded support: {KNOWN_REASONING_SUPPORT[model]} ✅")
        return KNOWN_REASONING_SUPPORT[model]

    # эмпирическая проверка (для будущих моделей)
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


@retry(
    stop=stop_after_attempt(4),                    # 4 попытки
    wait=wait_exponential(multiplier=3, min=5, max=30),  # 5s → 10s → 20s → 30s
    retry=retry_if_exception_type((json.JSONDecodeError, Exception)),  # ловим JSONDecode + любые другие
    reraise=True
)
def call_openrouter(domain, problem, model: str = "openai/gpt-5-mini", reasoning_enabled: bool = False):
    load_cache()

    # Если модель не поддерживает reasoning — выключаем
    if reasoning_enabled and not supports_reasoning(model):
        reasoning_enabled = False
        print(f"   ⚠️ reasoning отключён (модель не поддерживает)")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv('OPENROUTER_API_KEY'),
        timeout=1500.0,
    )

    def read_pddl(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    domain_text = read_pddl(domain)
    problem_text = read_pddl(problem)

    prompt = f'''You are a deterministic PDDL planner.

Goal: produce a valid plan that achieves the goal state with minimal number of actions.

Rules:
- Output ONLY the plan.
- One action per line.
- No extra text
- No empty lines
- Do NOT output anything before or after the plan.
- Stop immediately after the last action.

Constraints:
- The plan MUST be valid under the domain and problem.
- The plan SHOULD be optimal (minimum number of actions).
- Use only actions defined in the domain.
- Respect all preconditions and effects.

Strategy (internal, do not output):
- Reason step-by-step silently.
- Minimize the number of actions.
- Avoid redundant or reversing actions.

Domain:
{domain_text}

Problem:
{problem_text}

Return ONLY the plan.
Each line must contain exactly one action in PDDL format:
(action-name arg1 arg2 ...)
'''
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
        # final_plan = fix_plan_format(raw_content)

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