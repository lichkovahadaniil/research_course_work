import os
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential


load_dotenv()


MODEL_ALIASES = {
    "gpt-5-mini": "openai/gpt-5-mini",
    "grok-4.1-fast": "x-ai/grok-4.1-fast",
    "qwen/qwen3.5-35b-a3b:alibaba": "qwen/qwen3.5-35b-a3b:alibaba",
}
MODEL_CONFIG = {
    "openai/gpt-5-mini": {
        "max_tokens": None,
        "reasoning_effort": "medium",
    },
    "x-ai/grok-4.1-fast": {
        "max_tokens": None,
        "reasoning_effort": "medium",
    },
    "qwen/qwen3.5-35b-a3b:alibaba": {
        "max_tokens": None,
        "reasoning_effort": "medium",
        "temperature": 0.6,
        "top_p": 0.95,
        "top_k": 20,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.0,
        'repetition_penalty': 1.0
    },
}
RETRYABLE_EXCEPTIONS = (Exception,)


def fix_plan_format(plan_text: str) -> str:
    if not plan_text.strip():
        return plan_text

    fixed_lines = []
    for raw_line in plan_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("(") and line.endswith(")"):
            fixed_lines.append(line)
        else:
            fixed_lines.append(f"({line})")
    return "\n".join(fixed_lines)


def _resolve_provider_model(model: str) -> str:
    if model not in MODEL_ALIASES:
        raise ValueError(f"unsupported model: {model}")
    return MODEL_ALIASES[model]


def _read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=8, max=45),
    retry=retry_if_exception_type(RETRYABLE_EXCEPTIONS),
    reraise=True,
)
def call_openrouter(
    domain_path: str | Path,
    problem_path: str | Path,
    model: str = "gpt-5-mini",
    reasoning_enabled: bool = True,
    fix_plan_format_enabled: bool = False,
) -> dict[str, object]:
    provider_model = _resolve_provider_model(model)
    config = MODEL_CONFIG[provider_model]

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        timeout=1500.0,
    )

    prompt = f"""You are a deterministic PDDL planner.

Goal: produce a valid plan that achieves the goal state with minimal number of actions.

Rules:
- Output ONLY the plan.
- One action per line.
- No extra text.
- No empty lines.
- Stop immediately after the last action.

Constraints:
- The plan MUST be valid under the domain and problem.
- The plan SHOULD be optimal.
- Use only actions defined in the domain.
- Respect all preconditions and effects.

Domain:
{_read_text(domain_path)}

Problem:
{_read_text(problem_path)}

Return ONLY the plan.
Each line must contain exactly one action in PDDL format (use brackets):
(action-name arg1 arg2 ...)
"""

    extra_body = {}
    if reasoning_enabled:
        extra_body["reasoning"] = {"enabled": True}
        effort = config.get("reasoning_effort")
        if effort is not None:
            extra_body["reasoning"]["effort"] = effort

    create_kwargs = {
        "model": provider_model,
        "messages": [{"role": "user", "content": prompt}],
        "extra_body": extra_body,
        "temperature": config.get("temperature", 0.0),
        "max_tokens": config.get("max_tokens"),
        "top_p": config.get("top_p", 1.0),
    }
    for key in ("presence_penalty", "frequency_penalty"):
        if key in config:
            create_kwargs[key] = config[key]

    for key in ("top_k", "repetition_penalty"):
        if key in config:
            extra_body[key] = config[key]
            
    started_at = time.time()
    response = client.chat.completions.create(**create_kwargs)
    duration = round(time.time() - started_at, 2)

    message = response.choices[0].message
    raw_response = message.content or ""
    plan = fix_plan_format(raw_response) if fix_plan_format_enabled else raw_response

    reasoning_text = getattr(message, "reasoning", "") or ""
    if not reasoning_text and hasattr(message, "reasoning_details"):
        fragments = [
            item.get("text", "")
            for item in message.reasoning_details
            if isinstance(item, dict) and item.get("text")
        ]
        reasoning_text = "\n".join(fragments)

    return {
        "raw_response": raw_response,
        "plan": plan,
        "reasoning": reasoning_text,
        "reasoning_enabled": reasoning_enabled,
        "model": model,
        "duration_sec": duration,
        "prompt_tokens": getattr(response.usage, "prompt_tokens", None),
        "completion_tokens": getattr(response.usage, "completion_tokens", None),
        "total_tokens": getattr(response.usage, "total_tokens", None),
    }
