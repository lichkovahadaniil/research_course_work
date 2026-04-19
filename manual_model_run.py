import argparse
import json
from datetime import datetime
from pathlib import Path

from api_call import call_openrouter
from checker import build_metrics


MODEL_PROVIDER_MAP = {
    "xiaomi/mimo-v2-flash": "xiaomi/mimo-v2-flash:fp8",
    "qwen/qwen3.5-35b-a3b:alibaba": "qwen/qwen3.5-35b-a3b:alibaba",
}


def model_output_dir_name(model_name: str) -> str:
    return model_name.split("/")[-1].replace(":", "-").replace(".", "-")


def append_spending(res: dict, model: str, domain_file: Path, problem_file: Path) -> None:
    spendings_path = Path("spendings.json")
    entry = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "domain": str(domain_file),
        "problem": str(problem_file),
        "prompt_tokens": res.get("prompt_tokens"),
        "completion_tokens": res.get("completion_tokens"),
        "total_tokens": res.get("total_tokens"),
        "duration_sec": res.get("duration_sec"),
    }

    data = []
    if spendings_path.exists():
        try:
            with open(spendings_path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except json.JSONDecodeError:
            data = []

    data.append(entry)
    with open(spendings_path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)


def run_model(
    domain_path: Path,
    problem_path: Path,
    optimal_plan_path: Path,
    variant_dir: Path,
    model: str,
    force: bool,
) -> None:
    short_name = model_output_dir_name(model)
    model_dir = variant_dir / short_name
    model_dir.mkdir(parents=True, exist_ok=True)

    plan_path = model_dir / "llm.plan"
    result_path = model_dir / "llm_result.json"

    # === НОВАЯ ЛОГИКА ДЛЯ ЧАСТИЧНЫХ СБОЕВ ===
    if plan_path.exists() and result_path.exists() and not force:
        print(f"skip {variant_dir.name}/{short_name}: result already exists")
        return

    elif plan_path.exists() and not result_path.exists() and not force:
        print(f"⚠️  {variant_dir.name}/{short_name}: plan exists, but llm_result.json missing → rebuilding metrics only")
        # План уже есть — просто пересчитываем метрики
        metrics = build_metrics(domain_path, problem_path, plan_path, optimal_plan_path)

        # Собираем минимальный result_payload (без повторного вызова API)
        result_payload = {
            "model": model,
            "plan_file": str(plan_path),
            "metrics": metrics,
            # остальные поля (tokens, duration и т.д.) останутся None
            # если хочешь сохранить старые токены — можно читать старый json, но пока не нужно
        }
        with open(result_path, "w", encoding="utf-8") as handle:
            json.dump(result_payload, handle, ensure_ascii=False, indent=2)

        print(f"wrote {result_path} (metrics rebuilt)")
        return

    # === Обычный путь (вызов модели) ===
    provider_model = MODEL_PROVIDER_MAP.get(model, model)
    response = call_openrouter(domain_path, problem_path, model=provider_model, reasoning_enabled=True)

    with open(plan_path, "w", encoding="utf-8") as handle:
        handle.write(response["plan"])

    append_spending(response, model, domain_path, problem_path)

    metrics = build_metrics(domain_path, problem_path, plan_path, optimal_plan_path)
    result_payload = {
        **{key: value for key, value in response.items() if key != "plan"},
        "model": model,
        "plan_file": str(plan_path),
        "metrics": metrics,
    }
    with open(result_path, "w", encoding="utf-8") as handle:
        json.dump(result_payload, handle, ensure_ascii=False, indent=2)

    print(f"wrote {result_path}")
    

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run one manual model call and write its local artifacts.")
    parser.add_argument("--domain-path", required=True)
    parser.add_argument("--problem-path", required=True)
    parser.add_argument("--optimal-plan-path", required=True)
    parser.add_argument("--variant-dir", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--force", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    run_model(
        domain_path=Path(args.domain_path),
        problem_path=Path(args.problem_path),
        optimal_plan_path=Path(args.optimal_plan_path),
        variant_dir=Path(args.variant_dir),
        model=args.model,
        force=args.force,
    )


if __name__ == "__main__":
    main()
