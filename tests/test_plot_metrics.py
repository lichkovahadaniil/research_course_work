import json

from plot_metrics import build_records, build_reports, summarize_records


def write_result(root, domain, problem, variant, run_id, model, metrics, response_fields=None) -> None:
    from manual_model_run import model_output_dir_name

    result_dir = root / "materials" / domain / problem / variant / str(run_id) / model_output_dir_name(model)
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


def test_build_records_uses_new_metrics_only(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    write_result(
        tmp_path,
        "logistics",
        "p01",
        "frequency",
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
                "optimality_ratio": 1.25,
            },
        },
        {
            "completion_tokens": 120,
            "reasoning": "thought thought thought thought",
            "raw_response": "(move a b)",
        },
    )
    write_result(
        tmp_path,
        "logistics",
        "p01",
        "disp_1",
        2,
        "deepseek-v3.2",
        {
            "strict": {
                "plan_length": None,
                "executability": False,
                "reachability": False,
                "first_failure_step": 8,
                "non_executable_failure": "state_execution_error",
            },
            "legacy": {
                "optimality_ratio": None,
            },
        },
        {
            "completion_tokens": 80,
            "reasoning": "analysis step",
            "raw_response": "(move x y)",
        },
    )

    records = build_records(["logistics"], ["p01"])

    assert set(records.columns) == {
        "domain",
        "problem",
        "variant",
        "run",
        "model",
        "plan_length",
        "executability",
        "reachability",
        "conditional_reachability",
        "optimality_ratio",
        "first_failure_step",
        "non_executable_failure",
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "reasoning_completion_tokens",
        "raw_completion_tokens",
        "completion_token_breakdown_source",
    }
    assert len(records) == 2
    reachable_row = records[records["run"] == 1].iloc[0]
    failed_row = records[records["run"] == 2].iloc[0]
    assert reachable_row["plan_length"] == 4
    assert failed_row["plan_length"] != failed_row["plan_length"]
    assert failed_row["non_executable_failure"] == 1.0
    assert reachable_row["completion_tokens"] == 120
    assert reachable_row["reasoning_completion_tokens"] + reachable_row["raw_completion_tokens"] == 120
    assert reachable_row["completion_token_breakdown_source"] == "estimated_text_ratio"


def test_summarize_records_groups_by_variant_and_model() -> None:
    import pandas as pd

    records = pd.DataFrame(
        [
            {"variant": "frequency", "model": "grok-4.1-fast", "plan_length": 10},
            {"variant": "frequency", "model": "grok-4.1-fast", "plan_length": 14},
            {"variant": "disp_1", "model": "grok-4.1-fast", "plan_length": 8},
        ]
    )

    summary = summarize_records(records, "plan_length")

    assert len(summary) == 2
    assert summary.loc[summary["variant"] == "frequency", "plan_length"].iloc[0] == 12


def test_build_reports_writes_problem_barplots_only(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    write_result(
        tmp_path,
        "logistics",
        "p01",
        "frequency",
        1,
        "grok-4.1-fast",
        {
            "strict": {
                "plan_length": 3,
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
            "completion_tokens": 150,
            "reasoning_completion_tokens": 120,
            "raw_completion_tokens": 30,
        },
    )

    build_reports(["logistics"], ["p01"])

    assert (tmp_path / "materials" / "logistics" / "graph" / "p01" / "plan_length_barplot.png").exists()
    assert (
        tmp_path / "materials" / "logistics" / "graph" / "p01" / "completion_token_breakdown_barplot.png"
    ).exists()
    assert not (tmp_path / "materials" / "logistics" / "graph" / "summary").exists()
