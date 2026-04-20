from pathlib import Path

import pytest

from main import MODEL_NAMES, VARIANT_NAMES, build_run_commands, normalize_problem_ids, run_models


def create_prepared_problem(root: Path, domain_name: str, problem_id: str) -> None:
    problem_dir = root / "materials" / domain_name / problem_id
    problem_dir.mkdir(parents=True, exist_ok=True)
    (problem_dir / f"{problem_id}.pddl").write_text("(define (problem p))", encoding="utf-8")
    (problem_dir / f"{problem_id}.plan").write_text("(a)\n", encoding="utf-8")
    for variant_name in VARIANT_NAMES:
        variant_dir = problem_dir / variant_name
        variant_dir.mkdir(parents=True, exist_ok=True)
        (variant_dir / "domain.pddl").write_text("(define (domain d))", encoding="utf-8")


def test_build_run_commands_uses_new_matrix(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    create_prepared_problem(tmp_path, "folding", "p01")

    commands = build_run_commands(["folding"], ["p01"])

    assert len(commands) == len(VARIANT_NAMES) * len(MODEL_NAMES)
    assert all("manual_model_run.py" in command[1] for command in commands)
    assert {command[-1] for command in commands} == set(MODEL_NAMES)
    assert {Path(command[9]).name for command in commands} == set(VARIANT_NAMES)


def test_run_models_executes_every_command(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    create_prepared_problem(tmp_path, "labyrinth", "p03")

    executed: list[list[str]] = []

    def fake_run(command: list[str], check: bool) -> None:
        assert check is True
        executed.append(command)

    monkeypatch.setattr("subprocess.run", fake_run)
    run_models(["labyrinth"], ["p03"])

    assert len(executed) == len(VARIANT_NAMES) * len(MODEL_NAMES)


def test_normalize_problem_ids_defaults_to_all_problems() -> None:
    normalized = normalize_problem_ids(None)
    assert normalized[0] == "p01"
    assert normalized[-1] == "p20"
    assert len(normalized) == 20


def test_build_run_commands_requires_prepared_variants(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    problem_dir = tmp_path / "materials" / "folding" / "p01"
    problem_dir.mkdir(parents=True, exist_ok=True)
    (problem_dir / "p01.pddl").write_text("(define (problem p))", encoding="utf-8")
    (problem_dir / "p01.plan").write_text("(a)\n", encoding="utf-8")

    with pytest.raises(FileNotFoundError):
        build_run_commands(["folding"], ["p01"])
