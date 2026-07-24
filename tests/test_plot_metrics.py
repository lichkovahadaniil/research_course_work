import json

from experiment_config import (
    MODEL_NAMES,
    PLAN_LENGTH_GROUPS,
    PROBLEM_IDS,
    REFERENCE_PLAN_ACTION_COUNTS_BY_ID,
    ProblemRef,
    plan_length_group_for_problem,
    problem_ids_in_plan_length_group,
)
import plot_metrics
from plot_metrics import (
    MODERN_COLORS,
    build_records,
    build_reports,
    _model_color,
    _palette_for_model_count,
    _plot_problem_variant_bar,
    summarize_confidence_intervals,
    summarize_problem_type_records,
    summarize_records,
)

TEST_MODEL = MODEL_NAMES[0]


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


def test_palette_assigns_unique_color_to_each_configured_model() -> None:
    palette = _palette_for_model_count(MODERN_COLORS, len(MODEL_NAMES))

    assert len(palette) == len(MODEL_NAMES)
    assert len({color.lower() for color in palette}) == len(MODEL_NAMES)
    assert [_model_color(MODERN_COLORS, model) for model in MODEL_NAMES] == palette


def test_palette_expands_without_reusing_colors() -> None:
    palette = _palette_for_model_count(["#111111", "#222222", "#333333"], 4)

    assert len(palette) == 4
    assert len({color.lower() for color in palette}) == 4


def test_plan_length_groups_partition_configured_problems() -> None:
    grouped_problem_ids = [
        problem_id
        for group in PLAN_LENGTH_GROUPS
        for problem_id in problem_ids_in_plan_length_group(group)
    ]

    assert set(REFERENCE_PLAN_ACTION_COUNTS_BY_ID) == set(PROBLEM_IDS)
    assert len(grouped_problem_ids) == len(PROBLEM_IDS)
    assert set(grouped_problem_ids) == set(PROBLEM_IDS)
    assert [
        len(problem_ids_in_plan_length_group(group))
        for group in PLAN_LENGTH_GROUPS
    ] == [7, 7, 6]
    assert plan_length_group_for_problem("p12").group_id == "1"
    assert plan_length_group_for_problem("p13").group_id == "2"
    assert plan_length_group_for_problem("p4").group_id == "2"
    assert plan_length_group_for_problem("p5").group_id == "3"
    assert plan_length_group_for_problem("p7").group_id == "3"


def test_problem_variant_bar_uses_unique_color_per_model(tmp_path, monkeypatch) -> None:
    import pandas as pd
    from matplotlib.colors import to_hex

    captured_colors: list[str] = []

    def capture_savefig(*args, **kwargs) -> None:
        ax = plot_metrics.plt.gcf().axes[0]
        captured_colors.extend(
            to_hex(container.patches[0].get_facecolor())
            for container in ax.containers[: len(MODEL_NAMES)]
        )

    monkeypatch.setattr(plot_metrics.plt, "savefig", capture_savefig)
    frame = pd.DataFrame(
        [
            {
                "variant": "canonical",
                "model": model_name,
                "plan_length": model_index + 1,
            }
            for model_index, model_name in enumerate(MODEL_NAMES)
        ]
    )

    _plot_problem_variant_bar(
        frame,
        {"slug": "plan_length", "title": "Plan Length", "rate": False},
        tmp_path / "plot.png",
        "Plan Length",
    )

    assert len(captured_colors) == len(MODEL_NAMES)
    assert len(set(captured_colors)) == len(MODEL_NAMES)


def test_russian_problem_variant_bar_uses_report_labels(tmp_path, monkeypatch) -> None:
    import pandas as pd

    captured: dict[str, object] = {}

    def capture_savefig(*args, **kwargs) -> None:
        ax = plot_metrics.plt.gcf().axes[0]
        captured["xlabel"] = ax.get_xlabel()
        captured["ylabel"] = ax.get_ylabel()
        captured["title"] = ax.get_title()
        captured["ticks"] = [tick.get_text() for tick in ax.get_xticklabels()]
        captured["legend"] = [text.get_text() for text in ax.get_legend().get_texts()]
        captured["legend_title"] = ax.get_legend().get_title().get_text()
        captured["texts"] = [text.get_text() for text in ax.texts]

    monkeypatch.setattr(plot_metrics.plt, "savefig", capture_savefig)
    frame = pd.DataFrame(
        [
            {
                "variant": "canonical",
                "model": model_name,
                "plan_length": model_index + 1,
            }
            for model_index, model_name in enumerate(MODEL_NAMES)
        ]
    )

    _plot_problem_variant_bar(
        frame,
        {"slug": "plan_length", "title": "Plan Length", "rate": False},
        tmp_path / "plot.png",
        "Длина плана",
        russian=True,
    )

    assert captured["xlabel"] == ""
    assert captured["ylabel"] == "Значение метрики"
    assert captured["title"] == "Длина плана"
    assert captured["ticks"] == ["№0", "№1", "№2", "№3", "№4", "№5", "№6"]
    assert captured["legend"] == ["DeepSeek V4", "GPT-OSS-120B", "Nemotron 3 super"]
    assert captured["legend_title"] == ""
    assert captured["texts"] == []


def test_build_records_uses_new_metrics_only(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    write_result(
        tmp_path,
        "logistics",
        "alpha",
        "p7",
        "canonical",
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
        TEST_MODEL,
        {
            "strict": {
                "parsable": False,
                "plan_length": 12,
                "executability": False,
                "reachability": False,
                "first_failure_step": None,
                "non_executable_failure": "parse_error",
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
        TEST_MODEL,
        {
            "strict": {
                "parsable": True,
                "plan_length": 9,
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
        "execution_progress",
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
    assert unreachable_row["plan_length"] != unreachable_row["plan_length"]
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
            {"variant": "canonical", "model": TEST_MODEL, "plan_length": 10},
            {"variant": "canonical", "model": TEST_MODEL, "plan_length": 12},
            *[
                {"variant": "canonical", "model": TEST_MODEL, "plan_length": None}
                for _ in range(13)
            ],
            {"variant": "disp_1", "model": TEST_MODEL, "plan_length": 8},
        ]
    )

    summary = summarize_records(records, "plan_length")

    assert len(summary) == 2
    assert summary.loc[summary["variant"] == "canonical", "plan_length"].iloc[0] == 11


def test_summarize_problem_type_records_keeps_orders_separate() -> None:
    import pandas as pd

    records = pd.DataFrame(
        [
            {
                "problem_type": "s01_l53",
                "variant": "canonical",
                "model": TEST_MODEL,
                "plan_length": 10,
            },
            {
                "problem_type": "s01_l53",
                "variant": "canonical",
                "model": TEST_MODEL,
                "plan_length": 14,
            },
            {
                "problem_type": "s01_l53",
                "variant": "disp_1",
                "model": TEST_MODEL,
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
    canonical_test_model = summary[
        (summary["problem_type"] == "s01_l53")
        & (summary["variant"] == "canonical")
        & (summary["model"] == TEST_MODEL)
    ]
    disp_test_model = summary[
        (summary["problem_type"] == "s01_l53")
        & (summary["variant"] == "disp_1")
        & (summary["model"] == TEST_MODEL)
    ]
    assert canonical_test_model["plan_length"].iloc[0] == 12
    assert disp_test_model["plan_length"].iloc[0] == 30


def test_summarize_confidence_intervals_calculates_numeric_and_rate_intervals() -> None:
    import pandas as pd

    numeric_records = pd.DataFrame(
        [
            {"variant": "canonical", "model": TEST_MODEL, "plan_length": 10},
            {"variant": "canonical", "model": TEST_MODEL, "plan_length": 12},
            {"variant": "canonical", "model": TEST_MODEL, "plan_length": 14},
            {"variant": "canonical", "model": TEST_MODEL, "plan_length": 16},
        ]
    )
    numeric_summary = summarize_confidence_intervals(
        numeric_records,
        {"slug": "plan_length", "title": "Plan Length", "rate": False},
    )

    assert numeric_summary["mean"].iloc[0] == 13
    assert numeric_summary["n"].iloc[0] == 4
    assert numeric_summary["ci_method"].iloc[0] == "t_mean_95"
    assert numeric_summary["ci95_low"].iloc[0] < 13 < numeric_summary["ci95_high"].iloc[0]

    rate_records = pd.DataFrame(
        [
            {"variant": "canonical", "model": TEST_MODEL, "reachability": 1.0},
            {"variant": "canonical", "model": TEST_MODEL, "reachability": 1.0},
            {"variant": "canonical", "model": TEST_MODEL, "reachability": 0.0},
        ]
    )
    rate_summary = summarize_confidence_intervals(
        rate_records,
        {"slug": "reachability", "title": "Reachability", "rate": True},
    )

    assert rate_summary["mean"].iloc[0] == 2 / 3
    assert rate_summary["n"].iloc[0] == 3
    assert rate_summary["ci_method"].iloc[0] == "wilson_score_95"
    assert 0 <= rate_summary["ci95_low"].iloc[0] < 2 / 3
    assert 2 / 3 < rate_summary["ci95_high"].iloc[0] <= 1


def test_confidence_interval_plot_has_compact_labels_and_no_annotations(tmp_path, monkeypatch) -> None:
    import pandas as pd

    captured: dict[str, object] = {}

    def capture_savefig(*args, **kwargs) -> None:
        ax = plot_metrics.plt.gcf().axes[0]
        captured["texts"] = [text.get_text() for text in ax.texts]
        captured["xlabel"] = ax.get_xlabel()
        captured["ylabel"] = ax.get_ylabel()
        captured["title"] = ax.get_title()
        captured["legend_title"] = ax.get_legend().get_title().get_text()

    monkeypatch.setattr(plot_metrics.plt, "savefig", capture_savefig)
    frame = pd.DataFrame(
        [
            {"variant": "canonical", "model": TEST_MODEL, "reachability": 1.0},
            {"variant": "canonical", "model": TEST_MODEL, "reachability": 0.0},
        ]
    )

    plot_metrics._plot_confidence_intervals(
        frame,
        {"slug": "reachability", "title": "Reachability", "rate": True},
        tmp_path / "plot.png",
        "Reachability",
    )

    assert captured["texts"] == []
    assert captured["xlabel"] == "Metric value"
    assert captured["ylabel"] == ""
    assert captured["title"] == "Reachability"
    assert captured["legend_title"] == ""


def test_token_breakdown_plot_has_no_stack_percentage_annotations(tmp_path, monkeypatch) -> None:
    import pandas as pd
    from matplotlib.legend import Legend

    captured: dict[str, object] = {}

    def capture_savefig(*args, **kwargs) -> None:
        ax = plot_metrics.plt.gcf().axes[0]
        captured["texts"] = [text.get_text() for text in ax.texts]
        captured["xlabel"] = ax.get_xlabel()
        captured["ylabel"] = ax.get_ylabel()
        captured["legend_titles"] = [
            child.get_title().get_text()
            for child in ax.get_children()
            if isinstance(child, Legend)
        ]

    monkeypatch.setattr(plot_metrics.plt, "savefig", capture_savefig)
    frame = pd.DataFrame(
        [
            {
                "variant": "canonical",
                "model": TEST_MODEL,
                "completion_tokens": 100,
                "reasoning_completion_tokens": 60,
                "raw_completion_tokens": 40,
            }
        ]
    )

    plot_metrics._plot_problem_token_breakdown(
        frame,
        tmp_path / "plot.png",
        "Completion Token Breakdown",
    )

    assert captured["texts"] == []
    assert captured["xlabel"] == ""
    assert captured["ylabel"] == "Completion tokens"
    assert captured["legend_titles"] == ["", ""]


def test_build_reports_writes_technical_and_russian_graph_sets(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    for problem_id, plan_length in [("p1", 11), ("p3", 13)]:
        write_result(
            tmp_path,
            "logistics",
            "alpha",
            problem_id,
            "canonical",
            1,
            TEST_MODEL,
            {
                "strict": {
                    "plan_length": plan_length,
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
    write_result(
        tmp_path,
        "logistics",
        "alpha",
        "p7",
        "canonical",
        1,
        TEST_MODEL,
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

    build_reports(
        ["logistics"],
        [
            ProblemRef("alpha", "p1"),
            ProblemRef("alpha", "p3"),
            ProblemRef("alpha", "p7"),
        ],
    )

    graph_dir = tmp_path / "materials" / "logistics" / "graph"
    tech_problem_dir = graph_dir / "tech" / "cross_problem" / "p7"
    report_problem_dir = graph_dir / "report" / "cross_problem" / "p7"
    tech_means_dir = graph_dir / "tech" / "means"
    report_means_dir = graph_dir / "report" / "means"
    tech_groups_dir = graph_dir / "tech" / "groups"
    report_groups_dir = graph_dir / "report" / "groups"

    for problem_dir in [tech_problem_dir, report_problem_dir]:
        assert (problem_dir / "plan_length_barplot.png").exists()
        assert (problem_dir / "plan_length_confidence_intervals.png").exists()
        assert (problem_dir / "confidence_intervals.csv").exists()
        assert (problem_dir / "completion_token_breakdown_barplot.png").exists()

    for means_dir in [tech_means_dir, report_means_dir]:
        assert (means_dir / "plan_length_by_order_barplot.png").exists()
        assert (means_dir / "plan_length_by_order_confidence_intervals.png").exists()
        assert (means_dir / "confidence_intervals_by_order.csv").exists()
        assert (means_dir / "completion_token_breakdown_by_order_barplot.png").exists()

    assert (tech_problem_dir / "confidence_intervals.csv").read_bytes() == (
        report_problem_dir / "confidence_intervals.csv"
    ).read_bytes()
    assert (tech_means_dir / "confidence_intervals_by_order.csv").read_bytes() == (
        report_means_dir / "confidence_intervals_by_order.csv"
    ).read_bytes()

    for groups_dir in [tech_groups_dir, report_groups_dir]:
        assert (groups_dir / "README.md").exists()
        for group_id in ["1", "2", "3"]:
            group_dir = groups_dir / group_id
            assert (group_dir / "plan_length_by_order_barplot.png").exists()
            assert (group_dir / "plan_length_by_order_confidence_intervals.png").exists()
            assert (group_dir / "confidence_intervals_by_order.csv").exists()
            assert (group_dir / "completion_token_breakdown_by_order_barplot.png").exists()

    assert "# Reference-plan-length groups" in (tech_groups_dir / "README.md").read_text(encoding="utf-8")
    assert "# Группы по длине эталонного плана" in (report_groups_dir / "README.md").read_text(
        encoding="utf-8"
    )

    import pandas as pd

    for group_id, expected_mean in [("1", 11), ("2", 13), ("3", 3)]:
        tech_group_table = pd.read_csv(tech_groups_dir / group_id / "confidence_intervals_by_order.csv")
        plan_length_row = tech_group_table[
            (tech_group_table["metric"] == "plan_length")
            & (tech_group_table["variant"] == "canonical")
            & (tech_group_table["model"] == TEST_MODEL)
        ].iloc[0]
        assert plan_length_row["mean"] == expected_mean
        assert (tech_groups_dir / group_id / "confidence_intervals_by_order.csv").read_bytes() == (
            report_groups_dir / group_id / "confidence_intervals_by_order.csv"
        ).read_bytes()

    assert not (graph_dir / "alpha").exists()
    assert not (graph_dir / "design").exists()
    assert not (graph_dir / "plan_length_by_order_barplot.png").exists()
