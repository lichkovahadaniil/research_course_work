import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import fcntl

from checker import build_metrics


def model_output_dir_name(model_name: str) -> str:
    return model_name.split("/")[-1].replace(":", "-").replace(".", "-")


def atomic_write_text(path: Path, content: str) -> None:
    tmp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp_path.write_text(content, encoding="utf-8")
    os.replace(tmp_path, path)


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    tmp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp_path, path)


def update_status(status_path: Path, stage: str, **extra: Any) -> None:
    atomic_write_json(
        status_path,
        {
            "stage": stage,
            "timestamp": datetime.now().isoformat(),
            **extra,
        },
    )


def append_spending(response: dict[str, Any], model: str, domain_path: Path, problem_path: Path) -> None:
    spendings_path = Path("spendings.json")
    lock_path = spendings_path.with_suffix(".lock")
    entry = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "domain": str(domain_path),
        "problem": str(problem_path),
        "prompt_tokens": response.get("prompt_tokens"),
        "completion_tokens": response.get("completion_tokens"),
        "total_tokens": response.get("total_tokens"),
        "duration_sec": response.get("duration_sec"),
    }

    with open(lock_path, "w", encoding="utf-8") as lock_handle:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        try:
            if spendings_path.exists():
                try:
                    payload = json.loads(spendings_path.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    payload = []
            else:
                payload = []

            payload.append(entry)
            atomic_write_json(spendings_path, payload)
        finally:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)


def load_json_dict(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def result_is_complete(payload: dict[str, Any] | None) -> bool:
    if not payload:
        return False
    metrics = payload.get("metrics")
    return isinstance(metrics, dict) and {"strict", "legacy", "reference"}.issubset(metrics)


def build_result_payload(
    *,
    model: str,
    plan_path: Path,
    metrics: dict[str, Any] | None,
    response: dict[str, Any] | None = None,
    postprocess_error: dict[str, str] | None = None,
) -> dict[str, Any]:
    payload = {
        "model": model,
        "plan_file": str(plan_path),
        "metrics": metrics,
    }
    if response is not None:
        payload.update(
            {
                key: value
                for key, value in response.items()
                if key not in {"model", "plan", "plan_file", "metrics", "postprocess_error"}
            }
        )
    if postprocess_error is not None:
        payload["postprocess_error"] = postprocess_error
    return payload


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


def rebuild_result_from_existing_plan(
    *,
    model: str,
    plan_path: Path,
    result_path: Path,
    status_path: Path,
    domain_path: Path,
    problem_path: Path,
    optimal_plan_path: Path,
    existing_payload: dict[str, Any] | None,
) -> None:
    update_status(status_path, "rebuilding_from_existing_plan", plan_file=str(plan_path))
    metrics, postprocess_error = safe_build_metrics(domain_path, problem_path, plan_path, optimal_plan_path)
    payload = build_result_payload(
        model=model,
        plan_path=plan_path,
        metrics=metrics,
        response=existing_payload,
        postprocess_error=postprocess_error,
    )
    atomic_write_json(result_path, payload)
    update_status(status_path, "result_written_from_existing_plan", result_file=str(result_path))


def run_model(
    domain_path: Path,
    problem_path: Path,
    optimal_plan_path: Path,
    variant_dir: Path,
    model: str,
    force: bool,
) -> None:
    model_dir = variant_dir / model_output_dir_name(model)
    model_dir.mkdir(parents=True, exist_ok=True)

    plan_path = model_dir / "llm.plan"
    result_path = model_dir / "llm_result.json"
    status_path = model_dir / "run_status.json"
    existing_payload = load_json_dict(result_path)

    if plan_path.exists() and not force:
        if result_is_complete(existing_payload):
            update_status(status_path, "skipped_existing_result", result_file=str(result_path))
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

    from api_call import call_openrouter

    update_status(status_path, "calling_model", model=model)
    response = call_openrouter(
        domain_path=domain_path,
        problem_path=problem_path,
        model=model,
        reasoning_enabled=True,
    )

    atomic_write_text(plan_path, str(response["plan"]))
    update_status(status_path, "plan_written", plan_file=str(plan_path))

    metrics, postprocess_error = safe_build_metrics(domain_path, problem_path, plan_path, optimal_plan_path)
    payload = build_result_payload(
        model=model,
        plan_path=plan_path,
        metrics=metrics,
        response=response,
        postprocess_error=postprocess_error,
    )
    atomic_write_json(result_path, payload)
    update_status(status_path, "result_written", result_file=str(result_path))

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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run one model for one domain/problem/variant combination.")
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
