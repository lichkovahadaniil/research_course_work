from pathlib import Path

from main import collect_manual_run_commands


def test_collect_manual_run_commands_does_not_modify_workspace(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    variant_dir = tmp_path / "materials" / "folding" / "p01" / "canonical"
    variant_dir.mkdir(parents=True)
    (variant_dir / "domain.pddl").write_text("(define (domain d))", encoding="utf-8")
    problem_dir = variant_dir.parent
    (problem_dir / "p01.pddl").write_text("(define (problem p01))", encoding="utf-8")
    (problem_dir / "p01.plan").write_text("(a)\n", encoding="utf-8")

    before = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))
    commands = collect_manual_run_commands(
        domains=["folding"],
        problem_ids=["p01"],
        variants=["canonical"],
        models=["openai/gpt-5-mini"],
    )
    after = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))

    assert before == after
    assert len(commands) == 1
    assert "manual_model_run.py" in commands[0]
    assert "--model openai/gpt-5-mini" in commands[0]
