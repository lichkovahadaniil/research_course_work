import json

from experiment_config import ProblemRef
from plot_metrics import (
    build_records,
    build_reports,
    summarize_problem_type_records,
    summarize_records,
)


def write_result(root, domain, task, problem, variant, run_id, model, metrics, response_fields=None) -> None:
    from manual_model_run import model_output_dir_name

    result_dir = root / "materials" / domain / task / problem / variant / str(run_id) / model_output_dir_name(model)
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
        "alpha",
        "p7",
        "canonical",
        1,
        "deepseek-v4-flash",
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
        "alpha",
        "p7",
        "disp_1",
        2,
        "deepseek-v4-flash",
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
    write_result(
        tmp_path,
        "logistics",
        "alpha",
        "p7",
        "disp_1",
        3,
        "deepseek-v4-flash",
        {
            "strict": {
                "plan_length": None,
                "executability": True,
                "reachability": False,
                "first_failure_step": None,
                "non_executable_failure": None,
            },
            "legacy": {
                "optimality_ratio": None,
            },
        },
        {
            "completion_tokens": 90,
            "reasoning": "analysis step",
            "raw_response": "(move x y)\n(move y z)",
        },
    )

    records = build_records(["logistics"], [ProblemRef("alpha", "p7")])

    assert set(records.columns) == {
        "domain",
        "problem",
        "task",
        "problem_type",
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
    assert len(records) == 3
    reachable_row = records[records["run"] == 1].iloc[0]
    failed_row = records[records["run"] == 2].iloc[0]
    unreachable_row = records[records["run"] == 3].iloc[0]
    assert reachable_row["task"] == "alpha"
    assert reachable_row["problem_type"] == "s01_l53"
    assert reachable_row["plan_length"] == 4
    assert failed_row["plan_length"] != failed_row["plan_length"]
    assert failed_row["conditional_reachability"] != failed_row["conditional_reachability"]
    assert failed_row["non_executable_failure"] == 1.0
    assert unreachable_row["conditional_reachability"] == 0.0
    assert reachable_row["completion_tokens"] == 120
    assert reachable_row["reasoning_completion_tokens"] + reachable_row["raw_completion_tokens"] == 120
    assert reachable_row["completion_token_breakdown_source"] == "estimated_text_ratio"


def test_summarize_records_groups_by_variant_and_model() -> None:
    import pandas as pd

    records = pd.DataFrame(
        [
            {"variant": "canonical", "model": "deepseek-v4-flash", "plan_length": 10},
            {"variant": "canonical", "model": "deepseek-v4-flash", "plan_length": 14},
            {"variant": "disp_1", "model": "deepseek-v4-flash", "plan_length": 8},
        ]
    )

    summary = summarize_records(records, "plan_length")

    assert len(summary) == 2
    assert summary.loc[summary["variant"] == "canonical", "plan_length"].iloc[0] == 12


def test_summarize_problem_type_records_keeps_orders_separate() -> None:
    import pandas as pd

    records = pd.DataFrame(
        [
            {
                "problem_type": "s01_l53",
                "variant": "canonical",
                "model": "deepseek-v4-flash",
                "plan_length": 10,
            },
            {
                "problem_type": "s01_l53",
                "variant": "canonical",
                "model": "deepseek-v4-flash",
                "plan_length": 14,
            },
            {
                "problem_type": "s01_l53",
                "variant": "disp_1",
                "model": "deepseek-v4-flash",
                "plan_length": 30,
            },
            {
                "problem_type": "s01_l53",
                "variant": "canonical",
                "model": "glm-4.7-flash",
                "plan_length": 18,
            },
        ]
    )

    summary = summarize_problem_type_records(records, "plan_length")

    assert len(summary) == 3
    canonical_deepseek = summary[
        (summary["problem_type"] == "s01_l53")
        & (summary["variant"] == "canonical")
        & (summary["model"] == "deepseek-v4-flash")
    ]
    disp_deepseek = summary[
        (summary["problem_type"] == "s01_l53")
        & (summary["variant"] == "disp_1")
        & (summary["model"] == "deepseek-v4-flash")
    ]
    assert canonical_deepseek["plan_length"].iloc[0] == 12
    assert disp_deepseek["plan_length"].iloc[0] == 30


def test_build_reports_writes_problem_and_problem_type_barplots(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    write_result(
        tmp_path,
        "logistics",
        "alpha",
        "p7",
        "canonical",
        1,
        "deepseek-v4-flash",
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

    build_reports(["logistics"], [ProblemRef("alpha", "p7")])

    assert (
        tmp_path / "materials" / "logistics" / "graph" / "alpha" / "p7" / "plan_length_barplot.png"
    ).exists()
    assert (
        tmp_path
        / "materials"
        / "logistics"
        / "graph"
        / "alpha"
        / "p7"
        / "completion_token_breakdown_barplot.png"
    ).exists()
    assert (
        tmp_path
        / "materials"
        / "logistics"
        / "graph"
        / "by_problem_type"
        / "plan_length_by_problem_type_and_order_barplot.png"
    ).exists()
    assert (
        tmp_path
        / "materials"
        / "logistics"
        / "graph"
        / "by_problem_type"
        / "s01_l53"
        / "plan_length_barplot.png"
    ).exists()
