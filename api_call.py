import os
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from token_usage import build_token_usage_from_response


load_dotenv()


MODEL_ALIASES = {
    "deepseek/deepseek-v4-flash": "deepseek/deepseek-v4-flash",
    "gpt-oss-120b": "openai/gpt-oss-120b",
    "nemotron-3-super": "nvidia/nemotron-3-super-120b-a12b",
}
MODEL_CONFIG = {
    "deepseek/deepseek-v4-flash": {
        "max_tokens": None,
        "supports_reasoning": True,
        "reasoning_effort": "medium",
        "temperature": 1.0,
        "top_p": 1.0,
        "provider": {
            "order": ["atlas-cloud"],
            "allow_fallbacks": False,
            "quantizations": ["fp8"],
        },
    },
    "openai/gpt-oss-120b": {
        "max_tokens": None,
        "supports_reasoning": True,
        "reasoning_effort": "medium",
        "temperature": 1.0,
        "top_p": 1.0,
        "provider": {
            "order": ["DeepInfra"],
            "allow_fallbacks": False,
            "quantizations": ["bf16"],
        },
    },
    "nvidia/nemotron-3-super-120b-a12b": {
        "max_tokens": None,
        "supports_reasoning": True,
        "reasoning_effort": "medium",
        "temperature": 1.0,
        "top_p": 0.95,
        "provider": {
            "order": ["deepinfra"],
            "allow_fallbacks": False,
            "quantizations": ["bf16"],
        },
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
    model: str = "glm-4.7-flash",
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
- The plan MUST be complete.
- Do NOT stop early.
- Continue until the goal is achieved.
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
You must give an answer.
Each line must contain exactly one action in PDDL format. Also use brackets "()":
(action-name arg1 arg2 ...)
"""

    extra_body = {}
    reasoning_used = reasoning_enabled and config.get("supports_reasoning", True)
    if reasoning_used:
        extra_body["reasoning"] = {"enabled": True}
        effort = config.get("reasoning_effort")
        if effort is not None:
            extra_body["reasoning"]["effort"] = effort

    create_kwargs = {
        "model": provider_model,
        "messages": [{"role": "user", "content": prompt}],
        "extra_body": extra_body,
        "temperature": config.get("temperature", 0.0),
        "top_p": config.get("top_p", 1.0),
    }
    max_tokens = config.get("max_tokens")
    if max_tokens is not None:
        create_kwargs["max_tokens"] = max_tokens
    for key in ("presence_penalty", "frequency_penalty"):
        if key in config:
            create_kwargs[key] = config[key]

    for key in ("top_k", "min_p", "repetition_penalty", "provider"):
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
    token_usage = build_token_usage_from_response(
        response=response,
        reasoning_text=reasoning_text,
        raw_response=raw_response,
    )

    return {
        "raw_response": raw_response,
        "plan": plan,
        "reasoning": reasoning_text,
        "reasoning_enabled": reasoning_used,
        "model": model,
        "duration_sec": duration,
        **token_usage,
    }
