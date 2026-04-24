from pathlib import Path

import pytest

from main import MODEL_NAMES, build_run_commands, normalize_problem_ids, run_models
from manual_model_run import model_output_dir_name
from shuffler import VARIANT_NAMES


def create_prepared_problem(root: Path, domain_name: str, problem_id: str) -> None:
    problem_dir = root / "materials" / domain_name / problem_id
    problem_dir.mkdir(parents=True, exist_ok=True)
    (problem_dir / f"{problem_id}.pddl").write_text("(define (problem p))", encoding="utf-8")
    (problem_dir / f"{problem_id}.plan").write_text("(a)\n", encoding="utf-8")
    for variant_name in VARIANT_NAMES:
        variant_dir = problem_dir / variant_name
        variant_dir.mkdir(parents=True, exist_ok=True)
        (variant_dir / "domain.pddl").write_text("(define (domain d))", encoding="utf-8")


def test_build_run_commands_uses_requested_models_orders_and_runs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    create_prepared_problem(tmp_path, "labyrinth", "p01")

    commands = build_run_commands(["p01"], ["grok-4.1-fast"], ["frequency", "disp_3"], runs=2, force=False)

    assert len(commands) == 4
    assert all("manual_model_run.py" in command[1] for command in commands)
    assert {command[-1] for command in commands} == {"grok-4.1-fast"}
    assert {Path(command[9]).parent.name for command in commands} == {"1", "2"}
    assert {Path(command[9]).parent.parent.name for command in commands} == {"frequency", "disp_3"}
    assert {Path(command[9]).name for command in commands} == {model_output_dir_name("grok-4.1-fast")}


def test_build_run_commands_skips_existing_runs_without_force(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    create_prepared_problem(tmp_path, "labyrinth", "p01")
    existing_dir = tmp_path / "materials" / "labyrinth" / "p01" / "canonical" / "1" / model_output_dir_name("grok-4.1-fast")
    existing_dir.mkdir(parents=True, exist_ok=True)
    (existing_dir / "llm.plan").write_text("(a)\n", encoding="utf-8")

    commands = build_run_commands(["p01"], ["grok-4.1-fast"], ["canonical"], runs=4, force=False)

    assert len(commands) == 3
    assert {Path(command[9]).parent.name for command in commands} == {"2", "3", "4"}


def test_build_run_commands_keeps_existing_runs_with_force(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    create_prepared_problem(tmp_path, "labyrinth", "p01")
    existing_dir = tmp_path / "materials" / "labyrinth" / "p01" / "canonical" / "1" / model_output_dir_name("grok-4.1-fast")
    existing_dir.mkdir(parents=True, exist_ok=True)
    (existing_dir / "llm.plan").write_text("(a)\n", encoding="utf-8")

    commands = build_run_commands(["p01"], ["grok-4.1-fast"], ["canonical"], runs=2, force=True)

    assert len(commands) == 2
    assert all(command[-1] == "--force" for command in commands)


def test_run_models_executes_every_command(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    create_prepared_problem(tmp_path, "labyrinth", "p03")

    executed: list[list[str]] = []

    def fake_run(command: list[str], check: bool) -> None:
        assert check is True
        executed.append(command)

    monkeypatch.setattr("subprocess.run", fake_run)
    run_models(["p03"], ["grok-4.1-fast"], ["frequency", "disp_3"], runs=2)

    assert len(executed) == 4


def test_normalize_problem_ids_defaults_to_all_problems() -> None:
    normalized = normalize_problem_ids(None)
    assert normalized[0] == "p01"
    assert normalized[-1] == "p20"
    assert len(normalized) == 20


def test_build_run_commands_requires_prepared_variants(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    problem_dir = tmp_path / "materials" / "labyrinth" / "p01"
    problem_dir.mkdir(parents=True, exist_ok=True)
    (problem_dir / "p01.pddl").write_text("(define (problem p))", encoding="utf-8")
    (problem_dir / "p01.plan").write_text("(a)\n", encoding="utf-8")

    with pytest.raises(FileNotFoundError):
        build_run_commands(["p01"], MODEL_NAMES, ["canonical"], runs=1, force=False)
