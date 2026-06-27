from pathlib import Path

from checker import (
    _run_validator,
    _sanitize_plan_text_for_validation,
    build_metrics,
    legacy_validation,
    strict_validation,
    wrap_plan_text_lines,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> str:
    return (FIXTURE_DIR / name).read_text(encoding="utf-8")


def test_sanitize_plan_text_for_validation_removes_non_action_wrapper() -> None:
    plan_text = """
</think>

(create_candidate shift_candidate_alpha)
(allocate_vehicle_unit origin_availability_alpha vehicle_unit_alpha)
"""

    assert _sanitize_plan_text_for_validation(plan_text) == (
        "(create_candidate shift_candidate_alpha)\n"
        "(allocate_vehicle_unit origin_availability_alpha vehicle_unit_alpha)\n"
    )


def test_sanitize_plan_text_for_validation_leaves_clean_or_actionless_text_alone() -> None:
    assert _sanitize_plan_text_for_validation("(create_candidate shift_candidate_alpha)\n") is None
    assert _sanitize_plan_text_for_validation("I could not find a plan.\n") is None


def test_wrap_plan_text_lines_wraps_each_non_empty_line() -> None:
    plan_text = """
Here is the plan:
create_candidate shift_candidate_alpha
(allocate_vehicle_unit origin_availability_alpha vehicle_unit_alpha)
"""

    assert wrap_plan_text_lines(plan_text) == (
        "(Here is the plan:)\n"
        "(create_candidate shift_candidate_alpha)\n"
        "(allocate_vehicle_unit origin_availability_alpha vehicle_unit_alpha)\n"
    )


def test_wrap_plan_text_lines_converts_call_style_actions() -> None:
    plan_text = """
execute_schedule_dispatch(shift_candidate_alpha vehicle_unit_gamma dispatch_slot_alpha)
release_compliance_certificate(shift_candidate_alpha compliance_certificate_alpha)
"""

    assert wrap_plan_text_lines(plan_text) == (
        "(execute_schedule_dispatch shift_candidate_alpha vehicle_unit_gamma dispatch_slot_alpha)\n"
        "(release_compliance_certificate shift_candidate_alpha compliance_certificate_alpha)\n"
    )


def test_wrap_plan_text_lines_ignores_empty_text() -> None:
    assert wrap_plan_text_lines("\n\n") is None


def test_run_validator_uses_sanitized_plan_copy(tmp_path: Path, monkeypatch) -> None:
    plan_path = tmp_path / "llm.plan"
    plan_path.write_text(
        "\n</think>\n\n(create_candidate shift_candidate_alpha)\n",
        encoding="utf-8",
    )
    captured: dict[str, str] = {}

    class FakeProcess:
        pid = 12345

        def poll(self) -> int:
            return 0

        def kill(self) -> None:
            pass

    def fake_popen(command, stdout, **kwargs):
        captured["plan_path"] = command[-1]
        captured["plan_text"] = Path(command[-1]).read_text(encoding="utf-8")
        stdout.write(f"Checking plan: {command[-1]}\nPlan size: 1\nPlan valid\n")
        return FakeProcess()

    monkeypatch.setattr("checker.subprocess.Popen", fake_popen)

    output, timed_out = _run_validator("-v", "domain.pddl", "problem.pddl", plan_path)

    assert timed_out is False
    assert captured["plan_path"] != str(plan_path)
    assert captured["plan_text"] == "(create_candidate shift_candidate_alpha)\n"
    assert f"Checking plan: {plan_path}" in output
    assert captured["plan_path"] not in output


def test_strict_validation_parse_error(monkeypatch) -> None:
    monkeypatch.setattr("checker._run_validator", lambda *args, **kwargs: (load_fixture("strict_parse_error.txt"), False))
    parsed = strict_validation("domain.pddl", "problem.pddl", "plan.pddl")
    assert parsed["parsable"] is False
    assert parsed["executability"] is False
    assert parsed["reachability"] is False
    assert parsed["plan_length"] is None
    assert parsed["execution_progress"] == 0.0
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
    assert parsed["execution_progress"] == 2 / 4
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
    monkeypatch.setattr(
        "checker._load_reference_plan_stats",
        lambda *args, **kwargs: {
            "optimal_cost": 1.0,
            "optimal_plan_length": 1,
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
