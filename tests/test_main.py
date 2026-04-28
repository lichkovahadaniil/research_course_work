from pathlib import Path

import pytest

from experiment_config import ProblemRef
from main import DEFAULT_DOMAIN, MODEL_NAMES, build_parser, build_run_commands, normalize_problem_refs, run_models
from manual_model_run import model_output_dir_name
from shuffler import VARIANT_NAMES


def create_prepared_problem(root: Path, domain_name: str, problem_ref: ProblemRef) -> None:
    problem_dir = root / "materials" / domain_name / problem_ref.task / problem_ref.problem
    problem_dir.mkdir(parents=True, exist_ok=True)
    (problem_dir / f"{problem_ref.problem}.pddl").write_text("(define (problem p))", encoding="utf-8")
    (problem_dir / f"{problem_ref.problem}.plan").write_text("(a)\n", encoding="utf-8")
    for variant_name in VARIANT_NAMES:
        variant_dir = problem_dir / variant_name
        variant_dir.mkdir(parents=True, exist_ok=True)
        (variant_dir / "domain.pddl").write_text("(define (domain d))", encoding="utf-8")


def test_build_run_commands_uses_requested_models_orders_and_runs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    problem_ref = ProblemRef("alpha", "p1")
    create_prepared_problem(tmp_path, "logistics", problem_ref)

    commands = build_run_commands([problem_ref], ["grok-4.1-fast"], ["canonical", "disp_3"], runs=2, force=False)

    assert len(commands) == 4
    assert all("manual_model_run.py" in command[1] for command in commands)
    assert {command[-1] for command in commands} == {"grok-4.1-fast"}
    assert {Path(command[9]).parent.name for command in commands} == {"1", "2"}
    assert {Path(command[9]).parent.parent.name for command in commands} == {"canonical", "disp_3"}
    assert {Path(command[9]).parent.parent.parent.name for command in commands} == {"p1"}
    assert {Path(command[9]).parent.parent.parent.parent.name for command in commands} == {"alpha"}
    assert {Path(command[9]).name for command in commands} == {model_output_dir_name("grok-4.1-fast")}


def test_default_domain_and_top_level_force_use_logistics() -> None:
    args = build_parser().parse_args(["--force"])

    assert DEFAULT_DOMAIN == "logistics"
    assert args.command is None
    assert args.force is True


def test_build_run_commands_skips_existing_runs_without_force(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    problem_ref = ProblemRef("alpha", "p1")
    create_prepared_problem(tmp_path, "logistics", problem_ref)
    existing_dir = tmp_path / "materials" / "logistics" / "alpha" / "p1" / "canonical" / "1" / model_output_dir_name("grok-4.1-fast")
    existing_dir.mkdir(parents=True, exist_ok=True)
    (existing_dir / "llm.plan").write_text("(a)\n", encoding="utf-8")

    commands = build_run_commands([problem_ref], ["grok-4.1-fast"], ["canonical"], runs=4, force=False)

    assert len(commands) == 3
    assert {Path(command[9]).parent.name for command in commands} == {"2", "3", "4"}


def test_build_run_commands_keeps_existing_runs_with_force(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    problem_ref = ProblemRef("alpha", "p1")
    create_prepared_problem(tmp_path, "logistics", problem_ref)
    existing_dir = tmp_path / "materials" / "logistics" / "alpha" / "p1" / "canonical" / "1" / model_output_dir_name("grok-4.1-fast")
    existing_dir.mkdir(parents=True, exist_ok=True)
    (existing_dir / "llm.plan").write_text("(a)\n", encoding="utf-8")

    commands = build_run_commands([problem_ref], ["grok-4.1-fast"], ["canonical"], runs=2, force=True)

    assert len(commands) == 2
    assert all(command[-1] == "--force" for command in commands)


def test_run_models_executes_every_command(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    problem_ref = ProblemRef("north", "p3")
    create_prepared_problem(tmp_path, "logistics", problem_ref)

    executed: list[list[str]] = []

    def fake_run(command: list[str], check: bool) -> None:
        assert check is True
        executed.append(command)

    monkeypatch.setattr("subprocess.run", fake_run)
    run_models([problem_ref], ["grok-4.1-fast"], ["canonical", "disp_3"], runs=2)

    assert len(executed) == 4


def test_normalize_problem_refs_defaults_to_all_problems() -> None:
    normalized = normalize_problem_refs(None)
    assert normalized[0] == ProblemRef("alpha", "p1")
    assert normalized[-1] == ProblemRef("port", "p7")
    assert len(normalized) == 28


def test_normalize_problem_refs_parses_task_scoped_selection() -> None:
    normalized = normalize_problem_refs(["north", "p1", "p02", "alpha", "3"])

    assert normalized == [
        ProblemRef("north", "p1"),
        ProblemRef("north", "p2"),
        ProblemRef("alpha", "p3"),
    ]


def test_normalize_problem_refs_selects_whole_task_when_only_task_is_given() -> None:
    normalized = normalize_problem_refs(["cold"])

    assert normalized[0] == ProblemRef("cold", "p1")
    assert normalized[-1] == ProblemRef("cold", "p7")
    assert len(normalized) == 7


def test_build_run_commands_requires_prepared_variants(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    problem_ref = ProblemRef("alpha", "p1")
    problem_dir = tmp_path / "materials" / "logistics" / problem_ref.task / problem_ref.problem
    problem_dir.mkdir(parents=True, exist_ok=True)
    (problem_dir / "p1.pddl").write_text("(define (problem p))", encoding="utf-8")
    (problem_dir / "p1.plan").write_text("(a)\n", encoding="utf-8")

    with pytest.raises(FileNotFoundError):
        build_run_commands([problem_ref], MODEL_NAMES, ["canonical"], runs=1, force=False)
