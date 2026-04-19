from pathlib import Path
import shutil

import pytest

from checker import action_sequence_distance, build_metrics, parse_strict_validation_output, strict_validation


FIXTURE_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> str:
    return (FIXTURE_DIR / name).read_text(encoding="utf-8")


def test_parse_error_fixture() -> None:
    parsed = parse_strict_validation_output(load_fixture("strict_parse_error.txt"))
    assert parsed["parsable"] is False
    assert parsed["executability"] is False
    assert parsed["reachability"] is False
    assert parsed["non_executable_failure"] == "parse_error"
    assert parsed["first_failure_step"] is None


def test_state_execution_failure_fixture() -> None:
    parsed = parse_strict_validation_output(load_fixture("strict_state_execution_failure.txt"))
    assert parsed["parsable"] is True
    assert parsed["executability"] is False
    assert parsed["reachability"] is False
    assert parsed["non_executable_failure"] == "state_execution_error"
    assert parsed["first_failure_step"] == 2


def test_goal_not_reached_fixture() -> None:
    parsed = parse_strict_validation_output(load_fixture("strict_goal_not_reached.txt"))
    assert parsed["parsable"] is True
    assert parsed["executability"] is True
    assert parsed["reachability"] is False
    assert parsed["non_executable_failure"] is None
    assert parsed["strict_final_value"] is None


def test_valid_goal_reaching_fixture() -> None:
    parsed = parse_strict_validation_output(load_fixture("strict_valid_goal_reaching.txt"))
    assert parsed["parsable"] is True
    assert parsed["executability"] is True
    assert parsed["reachability"] is True
    assert parsed["strict_final_value"] == 7.0
    assert parsed["plan_length"] == 4


def test_order_metrics_are_non_negative_and_normalized(tmp_path: Path) -> None:
    optimal = tmp_path / "optimal.plan"
    llm = tmp_path / "llm.plan"

    optimal.write_text("(a x)\n(b y)\n(c z)\n", encoding="utf-8")
    llm.write_text("(a x)\n(c z)\n(c z)\n", encoding="utf-8")

    metrics = action_sequence_distance(llm, optimal)

    assert metrics["insertions"] >= 0
    assert metrics["deletions"] >= 0
    assert metrics["total_distance"] >= 0
    assert 0.0 <= metrics["normalized_distance"] <= 1.0


def test_invalid_plan_gap_is_null_on_real_artifact() -> None:
    metrics = build_metrics(
        "materials/folding/p10/random_01/domain.pddl",
        "materials/folding/p10/p10.pddl",
        "materials/folding/p10/random_01/gpt-5-mini/llm.plan",
        "materials/folding/p10/p10.plan",
    )

    assert metrics["strict"]["reachability"] is False
    assert metrics["legacy"]["cost"] is None
    assert metrics["legacy"]["gap"] is None


@pytest.mark.skipif(shutil.which("validate") is None, reason="VAL is not installed")
def test_strict_validation_extracts_first_failure_step_from_real_artifact() -> None:
    metrics = strict_validation(
        "materials/folding/p10/random_01/domain.pddl",
        "materials/folding/p10/p10.pddl",
        "materials/folding/p10/random_01/gpt-5-mini/llm.plan",
    )
    assert metrics["first_failure_step"] == 2


@pytest.mark.skipif(shutil.which("validate") is None, reason="VAL is not installed")
def test_strict_validation_extracts_final_value_from_real_artifact() -> None:
    metrics = strict_validation(
        "materials/folding/p01/frequency/domain.pddl",
        "materials/folding/p01/p01.pddl",
        "materials/folding/p01/frequency/gpt-5-mini/llm.plan",
    )
    assert metrics["strict_final_value"] == 7.0
