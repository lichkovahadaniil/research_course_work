import json
from pathlib import Path

from manual_model_run import model_output_dir_name, refresh_aggregate_for_model, safe_build_metrics

TEST_MODEL = "mistralai/mistral-small-2603"


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


def test_safe_build_metrics_reformats_executable_empty_plan_and_reruns(tmp_path: Path, monkeypatch) -> None:
    domain_path = tmp_path / "domain.pddl"
    problem_path = tmp_path / "problem.pddl"
    plan_path = tmp_path / "llm.plan"
    optimal_plan_path = tmp_path / "optimal.plan"
    domain_path.write_text("(define (domain d) (:action create_candidate))\n", encoding="utf-8")
    problem_path.write_text("(define (problem p))\n", encoding="utf-8")
    plan_path.write_text("create_candidate(shift_candidate_alpha)\n", encoding="utf-8")
    optimal_plan_path.write_text("(create_candidate shift_candidate_alpha)\n", encoding="utf-8")
    seen_plan_texts: list[str] = []

    def fake_build_metrics(*args, **kwargs):
        seen_plan_texts.append(plan_path.read_text(encoding="utf-8"))
        if len(seen_plan_texts) == 1:
            return {
                "strict": {
                    "plan_length": 0,
                    "executability": True,
                    "reachability": False,
                },
                "legacy": {},
                "reference": {},
            }
        return {
            "strict": {
                "plan_length": 1,
                "executability": True,
                "reachability": True,
            },
            "legacy": {},
            "reference": {},
        }

    monkeypatch.setattr("manual_model_run.build_metrics", fake_build_metrics)

    metrics, error = safe_build_metrics(domain_path, problem_path, plan_path, optimal_plan_path)

    assert error is None
    assert metrics is not None
    assert metrics["strict"]["plan_length"] == 1
    assert plan_path.read_text(encoding="utf-8") == "(create_candidate shift_candidate_alpha)\n"
    assert seen_plan_texts == [
        "create_candidate(shift_candidate_alpha)\n",
        "(create_candidate shift_candidate_alpha)\n",
    ]


def test_refresh_aggregate_for_model_writes_mean_and_std(tmp_path: Path) -> None:
    order_dir = tmp_path / "materials" / "logistics" / "alpha" / "p7" / "canonical"
    write_result(
        order_dir,
        1,
        TEST_MODEL,
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
        TEST_MODEL,
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

    refresh_aggregate_for_model(order_dir, TEST_MODEL)

    aggregate_path = order_dir / "aggregate" / f"{model_output_dir_name(TEST_MODEL)}.json"
    payload = json.loads(aggregate_path.read_text(encoding="utf-8"))

    assert payload["model"] == TEST_MODEL
    assert payload["run_count"] == 2
    assert payload["runs"] == [1, 2]
    assert payload["metrics"]["plan_length"]["count"] == 2
    assert payload["metrics"]["plan_length"]["mean"] == 5.0
    assert payload["metrics"]["executability"]["mean"] == 0.5
    assert payload["metrics"]["conditional_reachability"]["count"] == 1
    assert payload["metrics"]["conditional_reachability"]["mean"] == 1.0
    assert payload["metrics"]["first_failure_step"]["mean"] == 2.0
    assert payload["metrics"]["completion_tokens"]["mean"] == 110.0
    assert payload["metrics"]["reasoning_completion_tokens"]["mean"] > payload["metrics"]["raw_completion_tokens"]["mean"]
