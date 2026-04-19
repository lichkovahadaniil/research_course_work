import json
from pathlib import Path

from result_backfill import fill_missing_runtime_fields


def write_result(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_fill_missing_runtime_fields_uses_peer_variant_means(tmp_path: Path) -> None:
    problem_dir = tmp_path / "materials" / "folding" / "p01"
    target_variant = problem_dir / "random_05"
    peer_a = problem_dir / "canonical"
    peer_b = problem_dir / "dispersion"

    for variant_dir in (target_variant, peer_a, peer_b):
        variant_dir.mkdir(parents=True, exist_ok=True)
        (variant_dir / "domain.pddl").write_text("(define (domain d))", encoding="utf-8")

    model_dir_name = "gpt-5-mini"
    write_result(peer_a / model_dir_name / "llm_result.json", {
        "duration_sec": 100.0,
        "prompt_tokens": 1000,
        "completion_tokens": 400,
        "total_tokens": 1400,
        "reasoning_enabled": True,
    })
    write_result(peer_b / model_dir_name / "llm_result.json", {
        "duration_sec": 80.0,
        "prompt_tokens": 1200,
        "completion_tokens": 600,
        "total_tokens": 1800,
        "reasoning_enabled": True,
    })

    filled = fill_missing_runtime_fields(
        {"model": "openai/gpt-5-mini", "plan_file": "x", "metrics": {"strict": {}, "legacy": {}, "order": {}}},
        variant_dir=target_variant,
        model_dir_name=model_dir_name,
    )

    assert filled["duration_sec"] == 90.0
    assert filled["prompt_tokens"] == 1100
    assert filled["completion_tokens"] == 500
    assert filled["total_tokens"] == 1600
    assert filled["reasoning_enabled"] is True
    assert filled["runtime_backfill"]["peer_count"] == 2


def test_fill_missing_runtime_fields_preserves_existing_values(tmp_path: Path) -> None:
    problem_dir = tmp_path / "materials" / "folding" / "p01"
    target_variant = problem_dir / "random_05"
    peer = problem_dir / "canonical"

    for variant_dir in (target_variant, peer):
        variant_dir.mkdir(parents=True, exist_ok=True)
        (variant_dir / "domain.pddl").write_text("(define (domain d))", encoding="utf-8")

    model_dir_name = "mimo-v2-flash"
    write_result(peer / model_dir_name / "llm_result.json", {
        "duration_sec": 50.0,
        "prompt_tokens": 200,
        "completion_tokens": 100,
        "total_tokens": 300,
        "reasoning_enabled": False,
    })

    filled = fill_missing_runtime_fields(
        {
            "duration_sec": 77.0,
            "prompt_tokens": None,
            "completion_tokens": None,
            "total_tokens": None,
            "reasoning_enabled": True,
        },
        variant_dir=target_variant,
        model_dir_name=model_dir_name,
    )

    assert filled["duration_sec"] == 77.0
    assert filled["prompt_tokens"] == 200
    assert filled["completion_tokens"] == 100
    assert filled["total_tokens"] == 300
    assert filled["reasoning_enabled"] is True
