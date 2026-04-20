import json

from plot_metrics import build_records, build_reports, summarize_records


def write_result(root, domain, problem, variant, model, metrics) -> None:
    from manual_model_run import model_output_dir_name

    result_dir = root / "materials" / domain / problem / variant / model_output_dir_name(model)
    result_dir.mkdir(parents=True, exist_ok=True)
    (result_dir / "llm_result.json").write_text(
        json.dumps(
            {
                "model": model,
                "plan_file": str(result_dir / "llm.plan"),
                "metrics": metrics,
            }
        ),
        encoding="utf-8",
    )


def test_build_records_uses_new_metrics_only(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    write_result(
        tmp_path,
        "folding",
        "p01",
        "frequency",
        "gpt-5-mini",
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
    )
    write_result(
        tmp_path,
        "folding",
        "p01",
        "dispersion_01",
        "grok-4.1-fast",
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
    )

    records = build_records(["folding"], ["p01"])

    assert set(records.columns) == {
        "domain",
        "problem",
        "variant",
        "model",
        "plan_length",
        "executability",
        "reachability",
        "conditional_reachability",
        "optimality_ratio",
        "first_failure_step",
        "non_executable_failure",
    }
    assert len(records) == 2
    reachable_row = records[records["model"] == "gpt-5-mini"].iloc[0]
    failed_row = records[records["model"] == "grok-4.1-fast"].iloc[0]
    assert reachable_row["plan_length"] == 4
    assert failed_row["plan_length"] != failed_row["plan_length"]
    assert failed_row["non_executable_failure"] == 1.0


def test_summarize_records_groups_by_variant_and_model() -> None:
    import pandas as pd

    records = pd.DataFrame(
        [
            {"variant": "frequency", "model": "gpt-5-mini", "plan_length": 10},
            {"variant": "frequency", "model": "gpt-5-mini", "plan_length": 14},
            {"variant": "dispersion_01", "model": "gpt-5-mini", "plan_length": 8},
        ]
    )

    summary = summarize_records(records, "plan_length")

    assert len(summary) == 2
    assert summary.loc[summary["variant"] == "frequency", "plan_length"].iloc[0] == 12


def test_build_reports_writes_problem_and_summary_barplots(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    write_result(
        tmp_path,
        "labyrinth",
        "p01",
        "frequency",
        "gpt-5-mini",
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
    )

    build_reports(["labyrinth"], ["p01"])

    assert (tmp_path / "materials" / "labyrinth" / "graph" / "p01" / "plan_length_barplot.png").exists()
    assert (
        tmp_path
        / "materials"
        / "labyrinth"
        / "graph"
        / "summary"
        / "reachability_summary_barplot.png"
    ).exists()
