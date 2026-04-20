import json
import re
from pathlib import Path

from shuffler import VARIANT_NAMES, shuffle


TOY_DOMAIN = """(define (domain toy)
  (:requirements :strips)
  (:predicates (ready))

  (:action alpha
    :precondition ()
    :effect ()
  )

  (:action beta
    :precondition ()
    :effect ()
  )

  (:action gamma
    :precondition ()
    :effect ()
  )

  (:action delta
    :precondition ()
    :effect ()
  )

  (:action epsilon
    :precondition ()
    :effect ()
  )
)
"""

TOY_PROBLEM = """(define (problem toy-problem)
  (:domain toy)
  (:init)
  (:goal (and))
)
"""

TOY_PLAN = """(beta)
(alpha)
(beta)
(gamma)
(delta)
(epsilon)
"""


def extract_action_order(domain_path: Path) -> list[str]:
    return re.findall(r"\(\s*:action\s+([^\s)]+)", domain_path.read_text(encoding="utf-8"))


def test_shuffle_creates_frequency_and_dispersion_variants(tmp_path: Path) -> None:
    domain_path = tmp_path / "domain.pddl"
    problem_path = tmp_path / "p01.pddl"
    optimal_plan_path = tmp_path / "p01.plan"
    save_dir = tmp_path / "materials" / "toy" / "p01"

    domain_path.write_text(TOY_DOMAIN, encoding="utf-8")
    problem_path.write_text(TOY_PROBLEM, encoding="utf-8")
    optimal_plan_path.write_text(TOY_PLAN, encoding="utf-8")

    shuffle(domain_path, problem_path, optimal_plan_path, save_dir, seed=52, problem_id="p01")

    frequency_order = ["beta", "alpha", "gamma", "delta", "epsilon"]
    assert extract_action_order(save_dir / "frequency" / "domain.pddl") == frequency_order
    assert extract_action_order(save_dir / "dispersion_01" / "domain.pddl") == [
        "epsilon",
        "beta",
        "alpha",
        "gamma",
        "delta",
    ]
    assert extract_action_order(save_dir / "dispersion_05" / "domain.pddl") == frequency_order


def test_shuffle_meta_is_minimal(tmp_path: Path) -> None:
    domain_path = tmp_path / "domain.pddl"
    problem_path = tmp_path / "p01.pddl"
    optimal_plan_path = tmp_path / "p01.plan"
    save_dir = tmp_path / "materials" / "toy" / "p01"

    domain_path.write_text(TOY_DOMAIN, encoding="utf-8")
    problem_path.write_text(TOY_PROBLEM, encoding="utf-8")
    optimal_plan_path.write_text(TOY_PLAN, encoding="utf-8")

    shuffle(domain_path, problem_path, optimal_plan_path, save_dir, seed=99, problem_id="p01")

    metadata = json.loads((save_dir / "shuffle_meta.json").read_text(encoding="utf-8"))
    assert metadata == {
        "seed": 99,
        "problem_id": "p01",
        "variants": VARIANT_NAMES,
    }
