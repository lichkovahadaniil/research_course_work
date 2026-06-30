from materials.stats.run_statistical_tests import (
    analysis_plan_length,
    build_model_payload,
    conditional_binary_result,
    fisher_exact_two_sided_p,
)


def test_conditional_binary_result_uses_per_order_executable_denominators() -> None:
    rows = [
        {
            "model": "test-model",
            "order": "canonical",
            "problem": "p1",
            "run": 1,
            "executability": 1.0,
            "conditional_reachability": 1.0,
        },
        {
            "model": "test-model",
            "order": "variant",
            "problem": "p1",
            "run": 1,
            "executability": 1.0,
            "conditional_reachability": 0.0,
        },
        {
            "model": "test-model",
            "order": "canonical",
            "problem": "p1",
            "run": 2,
            "executability": 0.0,
            "conditional_reachability": None,
        },
        {
            "model": "test-model",
            "order": "variant",
            "problem": "p1",
            "run": 2,
            "executability": 1.0,
            "conditional_reachability": 1.0,
        },
        {
            "model": "test-model",
            "order": "canonical",
            "problem": "p1",
            "run": 3,
            "executability": 1.0,
            "conditional_reachability": 1.0,
        },
        {
            "model": "test-model",
            "order": "variant",
            "problem": "p1",
            "run": 3,
            "executability": 0.0,
            "conditional_reachability": None,
        },
    ]

    result = conditional_binary_result(
        rows,
        "test-model",
        "conditional_reachability",
        "canonical",
        "variant",
    )

    assert result["baseline_n"] == 2
    assert result["compared_n"] == 2
    assert result["baseline_successes"] == 2
    assert result["compared_successes"] == 1
    assert result["baseline_mean"] == 1.0
    assert result["compared_mean"] == 0.5
    assert result["requires_both_executable"] is False


def test_fisher_exact_two_sided_p_is_symmetric() -> None:
    p_value = fisher_exact_two_sided_p(8, 2, 1, 5)

    assert p_value == fisher_exact_two_sided_p(1, 5, 8, 2)
    assert 0.0 <= p_value <= 1.0


def test_analysis_plan_length_matches_graph_semantics() -> None:
    assert analysis_plan_length(
        {"parsable": True, "reachability": True, "plan_length": 7}
    ) == 7
    assert analysis_plan_length(
        {"parsable": True, "reachability": False, "plan_length": 7}
    ) is None
    assert analysis_plan_length(
        {"parsable": False, "reachability": False, "plan_length": 7}
    ) is None
    assert analysis_plan_length({}) is None


def test_model_payload_uses_only_canonical_as_baseline() -> None:
    def row(order: str, reachability: float, plan_length: float) -> dict:
        return {
            "model": "test-model",
            "problem": "p1",
            "run": 1,
            "order": order,
            "reachability": reachability,
            "executability": 1.0,
            "conditional_reachability": reachability,
            "non_executable_failure": 0.0,
            "plan_length": plan_length,
            "optimality_ratio": 1.0,
            "first_failure_step": None,
            "prompt_tokens": 100.0,
            "completion_tokens": 50.0,
            "reasoning_completion_tokens": 25.0,
            "raw_completion_tokens": 25.0,
            "total_tokens": 150.0,
            "duration_sec": 3.0,
        }

    payload = build_model_payload(
        [
            row("canonical", 1.0, 10.0),
            row("disp_1", 0.0, 12.0),
            row("plan_front", 1.0, 9.0),
        ],
        "test-model",
    )

    assert "extra_order_comparisons" not in payload
    assert payload["compared_orders"] == ["disp_1", "plan_front"]
    for family in (
        "binary_tests",
        "conditional_binary_tests",
        "numeric_tests",
        "problem_level_tests",
    ):
        assert {result["baseline_order"] for result in payload[family]} == {"canonical"}

    assert {
        result["compared_order"] for result in payload["problem_level_tests"]
    } == {"disp_1", "plan_front"}


def test_disp3_analysis_uses_problem_level_holm_and_run_level_mcnemar() -> None:
    def row(order: str, reachability: float) -> dict:
        return {
            "model": "test-model",
            "problem": "p1",
            "run": 1,
            "order": order,
            "reachability": reachability,
            "executability": 1.0,
            "conditional_reachability": reachability,
            "non_executable_failure": 0.0,
            "plan_length": 10.0,
            "optimality_ratio": 1.0,
            "first_failure_step": None,
            "prompt_tokens": 100.0,
            "completion_tokens": 50.0,
            "reasoning_completion_tokens": 25.0,
            "raw_completion_tokens": 25.0,
            "total_tokens": 150.0,
            "duration_sec": 3.0,
        }

    payload = build_model_payload(
        [
            row("canonical", 0.0),
            row("disp_1", 0.0),
            row("disp_3", 0.0),
            row("plan_front", 1.0),
        ],
        "test-model",
    )

    problem_level = payload["disp3_problem_level_tests"]
    run_level = payload["disp3_run_level_mcnemar_tests"]

    assert payload["disp3_baseline_orders"] == ["canonical", "disp_1", "plan_front"]
    assert {result["metric"] for result in problem_level} == {"reachability"}
    assert {result["baseline_order"] for result in problem_level} == {
        "canonical",
        "disp_1",
        "plan_front",
    }
    assert {result["compared_order"] for result in problem_level} == {"disp_3"}
    assert all(
        "p_value_sign_flip_permutation_holm" in result
        for result in problem_level
    )

    empirical_best_rows = [
        result for result in problem_level if result["is_empirical_best_comparison"]
    ]
    assert len(empirical_best_rows) == 1
    assert empirical_best_rows[0]["baseline_order"] == "plan_front"
    assert empirical_best_rows[0]["empirical_best_order"] == "plan_front"

    assert {result["test"] for result in run_level} == {"exact_mcnemar"}
    assert {result["baseline_order"] for result in run_level} == {
        "canonical",
        "disp_1",
        "plan_front",
    }
    assert {result["compared_order"] for result in run_level} == {"disp_3"}
    assert all("p_value_holm" in result for result in run_level)
