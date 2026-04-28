import json
from pathlib import Path

from domain_generation import _variants_are_up_to_date
from shuffler import VARIANT_NAMES


def create_variant_dirs(problem_dir: Path) -> None:
    for variant_name in VARIANT_NAMES:
        variant_dir = problem_dir / variant_name
        variant_dir.mkdir(parents=True, exist_ok=True)
        (variant_dir / "domain.pddl").write_text("(define (domain d))", encoding="utf-8")


def test_variants_are_not_up_to_date_for_legacy_metadata(tmp_path: Path) -> None:
    problem_dir = tmp_path / "materials" / "logistics" / "p01"
    create_variant_dirs(problem_dir)
    (problem_dir / "shuffle_meta.json").write_text(
        json.dumps(
            {
                "seed": 52,
                "problem_id": "p01",
                "variants": VARIANT_NAMES,
            }
        ),
        encoding="utf-8",
    )

    assert _variants_are_up_to_date(problem_dir) is False


def test_variants_are_up_to_date_for_metadata_with_orders(tmp_path: Path) -> None:
    problem_dir = tmp_path / "materials" / "logistics" / "p01"
    create_variant_dirs(problem_dir)
    (problem_dir / "shuffle_meta.json").write_text(
        json.dumps(
            {
                "seed": 52,
                "problem_id": "p01",
                "variants": VARIANT_NAMES,
                "variant_orders": {
                    "canonical": ["a", "b", "c"],
                    "frequency": ["b", "a", "c"],
                    "disp_1": ["c", "b", "a"],
                    "disp_2": ["c", "a", "b"],
                    "disp_3": ["c", "b", "a"],
                },
            }
        ),
        encoding="utf-8",
    )

    assert _variants_are_up_to_date(problem_dir) is True
