from pathlib import Path

from checker import build_metrics, legacy_validation, strict_validation


FIXTURE_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> str:
    return (FIXTURE_DIR / name).read_text(encoding="utf-8")


def test_strict_validation_parse_error(monkeypatch) -> None:
    monkeypatch.setattr("checker._run_validator", lambda *args, **kwargs: (load_fixture("strict_parse_error.txt"), False))
    parsed = strict_validation("domain.pddl", "problem.pddl", "plan.pddl")
    assert parsed["parsable"] is False
    assert parsed["executability"] is False
    assert parsed["reachability"] is False
    assert parsed["plan_length"] is None
    assert parsed["non_executable_failure"] == "parse_error"


def test_strict_validation_state_execution_failure(monkeypatch) -> None:
    monkeypatch.setattr(
        "checker._run_validator",
        lambda *args, **kwargs: (load_fixture("strict_state_execution_failure.txt"), False),
    )
    parsed = strict_validation("domain.pddl", "problem.pddl", "plan.pddl")
    assert parsed["parsable"] is True
    assert parsed["executability"] is False
    assert parsed["reachability"] is False
    assert parsed["first_failure_step"] == 2
    assert parsed["non_executable_failure"] == "state_execution_error"


def test_legacy_validation_reads_cost(monkeypatch) -> None:
    monkeypatch.setattr(
        "checker._run_validator",
        lambda *args, **kwargs: (load_fixture("strict_valid_goal_reaching.txt"), False),
    )
    parsed = legacy_validation("domain.pddl", "problem.pddl", "plan.pddl")
    assert parsed["cost"] == 7.0
    assert parsed["goal_reached"] is True


def test_build_metrics_skips_cost_for_unreachable_plan(tmp_path: Path, monkeypatch) -> None:
    optimal_plan = tmp_path / "p01.plan"
    optimal_plan.write_text("(a)\n", encoding="utf-8")

    monkeypatch.setattr(
        "checker.strict_validation",
        lambda *args, **kwargs: {
            "parsable": True,
            "plan_length": None,
            "executability": False,
            "reachability": False,
            "first_failure_step": 3,
            "non_executable_failure": "state_execution_error",
            "strict_final_value": None,
            "validator_timed_out": False,
            "validator_stdout_strict": "failed",
        },
    )

    metrics = build_metrics("domain.pddl", "problem.pddl", "plan.pddl", optimal_plan)

    assert "order" not in metrics
    assert metrics["strict"]["plan_length"] is None
    assert metrics["legacy"]["cost"] is None
    assert metrics["legacy"]["optimality_ratio"] is None


def test_build_metrics_computes_optimality_ratio_for_reachable_plan(tmp_path: Path, monkeypatch) -> None:
    optimal_plan = tmp_path / "p01.plan"
    optimal_plan.write_text("(a)\n(b)\n", encoding="utf-8")

    monkeypatch.setattr(
        "checker.strict_validation",
        lambda *args, **kwargs: {
            "parsable": True,
            "plan_length": 2,
            "executability": True,
            "reachability": True,
            "first_failure_step": None,
            "non_executable_failure": None,
            "strict_final_value": 7.0,
            "validator_timed_out": False,
            "validator_stdout_strict": "ok",
        },
    )
    monkeypatch.setattr(
        "checker.legacy_validation",
        lambda *args, **kwargs: {
            "cost": 6.0,
            "goal_reached": True,
            "validator_timed_out": False,
            "validator_stdout_legacy": "ok",
        },
    )
    monkeypatch.setattr(
        "checker._load_reference_plan_stats",
        lambda *args, **kwargs: {
            "optimal_cost": 3.0,
            "optimal_plan_length": 2,
        },
    )

    metrics = build_metrics("domain.pddl", "problem.pddl", "plan.pddl", optimal_plan)

    assert metrics["strict"]["plan_length"] == 2
    assert metrics["legacy"]["cost"] == 6.0
    assert metrics["legacy"]["optimality_ratio"] == 2.0
    assert metrics["reference"]["optimal_plan_length"] == 2
