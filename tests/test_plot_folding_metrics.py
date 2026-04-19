import json

import pandas as pd

from plot_folding_metrics import build_records, resolve_problem_filters, summarize_records


def test_build_records_respects_problem_filter() -> None:
    records = build_records(["folding"], problem_ids=["p01"])

    assert not records.empty
    assert set(records["problem"]) == {"p01"}


def test_build_records_exposes_plot_columns() -> None:
    records = build_records(["folding"], problem_ids=["p01"])

    expected_columns = {
        "parsable",
        "executability",
        "reachability",
        "conditional_reachability",
        "non_executable_failure",
        "non_executable_failure_parse_share",
        "plan_length_metric",
        "legacy_cost",
        "legacy_gap",
        "optimality_ratio",
        "normalized_distance",
        "deprecated_kendall_tau_inversions",
        "duration_sec",
        "total_tokens",
    }

    assert expected_columns.issubset(records.columns)


def test_summarize_records_respects_metric_denominators() -> None:
    records = pd.DataFrame([
        {
            "domain": "folding",
            "problem": "p01",
            "variant": "canonical",
            "model": "gpt-5-mini",
            "plan_length_metric": 70,
            "executability": True,
            "reachability": True,
            "conditional_reachability": True,
            "first_failure_step": None,
            "optimality_ratio": 1.0,
            "non_executable_failure_parse_share": None,
        },
        {
            "domain": "folding",
            "problem": "p05",
            "variant": "canonical",
            "model": "gpt-5-mini",
            "plan_length_metric": None,
            "executability": False,
            "reachability": False,
            "conditional_reachability": None,
            "first_failure_step": 8,
            "optimality_ratio": None,
            "non_executable_failure_parse_share": 0.0,
        },
    ])

    summary = summarize_records(records, ["domain", "variant", "model"])
    row = summary.iloc[0]

    assert row["plan_length_metric"] == 70
    assert row["executability"] == 0.5
    assert row["reachability"] == 0.5
    assert row["conditional_reachability"] == 1.0
    assert row["first_failure_step"] == 8
    assert row["optimality_ratio"] == 1.0
    assert row["non_executable_failure_parse_share"] == 0.0
    assert row["problems_covered"] == 2


def test_resolve_problem_filters_prefers_metric_metadata(tmp_path, monkeypatch) -> None:
    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()
    (materials_dir / "metric.json").write_text(
        json.dumps({
            "_meta": {
                "domains": {
                    "folding": {
                        "selected_problems": ["p01", "p05"],
                    }
                }
            }
        }),
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    assert resolve_problem_filters(["folding", "labyrinth"]) == {
        "folding": ["p01", "p05"],
        "labyrinth": None,
    }
