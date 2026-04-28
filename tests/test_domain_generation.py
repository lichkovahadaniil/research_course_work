import json
from pathlib import Path

from domain_generation import _variants_are_up_to_date
from experiment_config import ProblemRef
from shuffler import VARIANT_NAMES


def create_variant_dirs(problem_dir: Path) -> None:
    for variant_name in VARIANT_NAMES:
        variant_dir = problem_dir / variant_name
        variant_dir.mkdir(parents=True, exist_ok=True)
        (variant_dir / "domain.pddl").write_text("(define (domain d))", encoding="utf-8")


def test_variants_are_not_up_to_date_for_legacy_metadata(tmp_path: Path) -> None:
    problem_ref = ProblemRef("alpha", "p1")
    problem_dir = tmp_path / "materials" / "logistics" / problem_ref.task / problem_ref.problem
    create_variant_dirs(problem_dir)
    (problem_dir / "shuffle_meta.json").write_text(
        json.dumps(
            {
                "seed": 52,
                "problem_id": "p1",
                "variants": VARIANT_NAMES,
            }
        ),
        encoding="utf-8",
    )

    assert _variants_are_up_to_date(problem_dir, problem_ref) is False


def test_variants_are_up_to_date_for_metadata_with_orders(tmp_path: Path) -> None:
    problem_ref = ProblemRef("alpha", "p1")
    problem_dir = tmp_path / "materials" / "logistics" / problem_ref.task / problem_ref.problem
    create_variant_dirs(problem_dir)
    (problem_dir / "shuffle_meta.json").write_text(
        json.dumps(
            {
                "seed": 52,
                "problem_id": "p1",
                "task": "alpha",
                "variants": VARIANT_NAMES,
                "variant_orders": {
                    "canonical": ["a", "b", "c"],
                    "disp_1": ["c", "b", "a"],
                    "disp_2": ["c", "a", "b"],
                    "disp_3": ["c", "b", "a"],
                },
            }
        ),
        encoding="utf-8",
    )

    assert _variants_are_up_to_date(problem_dir, problem_ref) is True
