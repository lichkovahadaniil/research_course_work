import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import fcntl

from checker import build_metrics
from result_backfill import fill_missing_runtime_fields, load_json_dict, result_payload_is_complete


MODEL_PROVIDER_MAP = {
    "xiaomi/mimo-v2-flash": "xiaomi/mimo-v2-flash:fp8",
    "qwen/qwen3.5-35b-a3b:alibaba": "qwen/qwen3.5-35b-a3b:alibaba",
}


def model_output_dir_name(model_name: str) -> str:
    return model_name.split("/")[-1].replace(":", "-").replace(".", "-")


def atomic_write_text(path: Path, content: str) -> None:
    tmp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with open(tmp_path, "w", encoding="utf-8") as handle:
        handle.write(content)
    os.replace(tmp_path, path)


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    tmp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with open(tmp_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)


def update_status(status_path: Path, stage: str, **extra: Any) -> None:
    payload = {
        "stage": stage,
        "timestamp": datetime.now().isoformat(),
        **extra,
    }
    atomic_write_json(status_path, payload)


def append_spending(res: dict, model: str, domain_file: Path, problem_file: Path) -> None:
    spendings_path = Path("spendings.json")
    lock_path = spendings_path.with_suffix(".lock")
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

    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_path, "w", encoding="utf-8") as lock_handle:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        try:
            data = []
            if spendings_path.exists():
                try:
                    with open(spendings_path, "r", encoding="utf-8") as handle:
                        data = json.load(handle)
                except json.JSONDecodeError:
                    data = []

            data.append(entry)
            atomic_write_json(spendings_path, data)
        finally:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)


def safe_build_metrics(
    domain_path: Path,
    problem_path: Path,
    plan_path: Path,
    optimal_plan_path: Path,
) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    try:
        return build_metrics(domain_path, problem_path, plan_path, optimal_plan_path), None
    except Exception as exc:
        return None, {
            "type": type(exc).__name__,
            "message": str(exc),
        }


def build_result_payload(
    model: str,
    plan_path: Path,
    metrics: dict[str, Any] | None,
    response: dict[str, Any] | None = None,
    postprocess_error: dict[str, str] | None = None,
) -> dict[str, Any]:
    base_payload = {
        "model": model,
        "plan_file": str(plan_path),
        "metrics": metrics,
    }
    if response is not None:
        base_payload.update({
            key: value
            for key, value in response.items()
            if key not in {"plan", "model", "plan_file", "metrics", "postprocess_error"}
        })
    if postprocess_error is not None:
        base_payload["postprocess_error"] = postprocess_error
    return base_payload


def rebuild_result_from_existing_plan(
    model: str,
    plan_path: Path,
    result_path: Path,
    status_path: Path,
    domain_path: Path,
    problem_path: Path,
    optimal_plan_path: Path,
    existing_payload: dict[str, Any] | None = None,
) -> None:
    print(f"⚠️  {plan_path.parent.parent.name}/{plan_path.parent.name}: plan exists, rebuilding llm_result.json only")
    update_status(status_path, "rebuilding_from_existing_plan", plan_file=str(plan_path))
    partial_payload = build_result_payload(
        model=model,
        plan_path=plan_path,
        metrics=None,
        response=existing_payload,
    )
    partial_payload = fill_missing_runtime_fields(
        partial_payload,
        variant_dir=plan_path.parent.parent,
        model_dir_name=plan_path.parent.name,
    )
    atomic_write_json(result_path, partial_payload)
    update_status(status_path, "metrics_started_for_existing_plan", result_file=str(result_path))

    metrics, postprocess_error = safe_build_metrics(domain_path, problem_path, plan_path, optimal_plan_path)
    result_payload = build_result_payload(
        model=model,
        plan_path=plan_path,
        metrics=metrics,
        response=partial_payload,
        postprocess_error=postprocess_error,
    )
    result_payload = fill_missing_runtime_fields(
        result_payload,
        variant_dir=plan_path.parent.parent,
        model_dir_name=plan_path.parent.name,
    )
    atomic_write_json(result_path, result_payload)
    update_status(status_path, "result_written_from_existing_plan", result_file=str(result_path))
    print(f"wrote {result_path}")


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
    status_path = model_dir / "run_status.json"

    existing_payload = load_json_dict(result_path)
    if plan_path.exists() and not force:
        if result_payload_is_complete(existing_payload):
            update_status(status_path, "skipped_existing_result", result_file=str(result_path))
            print(f"skip {variant_dir.name}/{short_name}: result already exists")
            return

        rebuild_result_from_existing_plan(
            model=model,
            plan_path=plan_path,
            result_path=result_path,
            status_path=status_path,
            domain_path=domain_path,
            problem_path=problem_path,
            optimal_plan_path=optimal_plan_path,
            existing_payload=existing_payload,
        )
        return

    provider_model = MODEL_PROVIDER_MAP.get(model, model)
    update_status(status_path, "calling_model", requested_model=model, provider_model=provider_model)
    from api_call import call_openrouter

    response = call_openrouter(domain_path, problem_path, model=provider_model, reasoning_enabled=True)

    update_status(status_path, "model_response_received")
    atomic_write_text(plan_path, response["plan"])
    update_status(status_path, "plan_written", plan_file=str(plan_path))

    partial_payload = build_result_payload(
        model=model,
        plan_path=plan_path,
        metrics=None,
        response=response,
    )
    partial_payload = fill_missing_runtime_fields(
        partial_payload,
        variant_dir=variant_dir,
        model_dir_name=short_name,
    )
    atomic_write_json(result_path, partial_payload)
    update_status(status_path, "partial_result_written", result_file=str(result_path))

    metrics, postprocess_error = safe_build_metrics(domain_path, problem_path, plan_path, optimal_plan_path)
    update_status(status_path, "metrics_built" if postprocess_error is None else "metrics_failed", postprocess_error=postprocess_error)

    result_payload = build_result_payload(
        model=model,
        plan_path=plan_path,
        metrics=metrics,
        response=partial_payload,
        postprocess_error=postprocess_error,
    )
    result_payload = fill_missing_runtime_fields(
        result_payload,
        variant_dir=variant_dir,
        model_dir_name=short_name,
    )
    atomic_write_json(result_path, result_payload)
    update_status(status_path, "result_written", result_file=str(result_path))
    print(f"wrote {result_path}")

    try:
        append_spending(response, model, domain_path, problem_path)
        update_status(status_path, "completed", spendings_logged=True)
    except Exception as exc:
        update_status(
            status_path,
            "completed_with_spending_error",
            spendings_logged=False,
            spending_error={"type": type(exc).__name__, "message": str(exc)},
        )
        print(f"warning: spendings log failed for {variant_dir.name}/{short_name}: {exc}")


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
