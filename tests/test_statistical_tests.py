from materials.stats.run_statistical_tests import (
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
