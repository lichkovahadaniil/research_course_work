import json
from pathlib import Path

from manual_model_run import model_output_dir_name, refresh_aggregate_for_model


def write_result(order_dir: Path, run_id: int, model: str, metrics: dict, response_fields=None) -> None:
    result_dir = order_dir / str(run_id) / model_output_dir_name(model)
    result_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "model": model,
        "plan_file": str(result_dir / "llm.plan"),
        "metrics": metrics,
    }
    if response_fields:
        payload.update(response_fields)
    (result_dir / "llm_result.json").write_text(
        json.dumps(payload),
        encoding="utf-8",
    )


def test_refresh_aggregate_for_model_writes_mean_and_std(tmp_path: Path) -> None:
    order_dir = tmp_path / "materials" / "logistics" / "alpha" / "p7" / "canonical"
    write_result(
        order_dir,
        1,
        "grok-4.1-fast",
        {
            "strict": {
                "plan_length": 4,
                "executability": True,
                "reachability": True,
                "first_failure_step": None,
                "non_executable_failure": None,
            },
            "legacy": {
                "optimality_ratio": 1.0,
            },
        },
        {
            "completion_tokens": 120,
            "reasoning_completion_tokens": 90,
            "raw_completion_tokens": 30,
        },
    )
    write_result(
        order_dir,
        2,
        "grok-4.1-fast",
        {
            "strict": {
                "plan_length": 6,
                "executability": False,
                "reachability": False,
                "first_failure_step": 2,
                "non_executable_failure": "state_execution_error",
            },
            "legacy": {
                "optimality_ratio": None,
            },
        },
        {
            "completion_tokens": 100,
            "reasoning": "thinking hard about path",
            "raw_response": "(move a b)",
        },
    )

    refresh_aggregate_for_model(order_dir, "grok-4.1-fast")

    aggregate_path = order_dir / "aggregate" / f"{model_output_dir_name('grok-4.1-fast')}.json"
    payload = json.loads(aggregate_path.read_text(encoding="utf-8"))

    assert payload["model"] == "grok-4.1-fast"
    assert payload["run_count"] == 2
    assert payload["runs"] == [1, 2]
    assert payload["metrics"]["plan_length"]["count"] == 1
    assert payload["metrics"]["plan_length"]["mean"] == 4.0
    assert payload["metrics"]["executability"]["mean"] == 0.5
    assert payload["metrics"]["first_failure_step"]["mean"] == 2.0
    assert payload["metrics"]["completion_tokens"]["mean"] == 110.0
    assert payload["metrics"]["reasoning_completion_tokens"]["mean"] > payload["metrics"]["raw_completion_tokens"]["mean"]
