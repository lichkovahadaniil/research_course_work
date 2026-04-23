import json
import shutil
from pathlib import Path

from experiment_config import DOMAIN_TYPES, PROBLEM_IDS
from shuffler import VARIANT_NAMES, shuffle


def _normalize_problem_ids(problems: list[str] | None = None) -> list[str]:
    return PROBLEM_IDS[:] if problems is None else sorted(set(problems))


def _cleanup_problem_variants(problem_dir: Path) -> None:
    for child in problem_dir.iterdir():
        if not child.is_dir():
            continue
        if child.name in VARIANT_NAMES or (child / "domain.pddl").exists():
            shutil.rmtree(child)


def _variants_are_up_to_date(problem_dir: Path) -> bool:
    metadata_path = problem_dir / "shuffle_meta.json"
    if not metadata_path.exists():
        return False

    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False

    if metadata.get("variants") != VARIANT_NAMES:
        return False

    variant_orders = metadata.get("variant_orders")
    if not isinstance(variant_orders, dict):
        return False
    if list(variant_orders) != VARIANT_NAMES:
        return False
    if not all(isinstance(order, list) and order for order in variant_orders.values()):
        return False

    return all((problem_dir / variant_name / "domain.pddl").exists() for variant_name in VARIANT_NAMES)


def generate_paths(domains: list[str] | None = None, problems: list[str] | None = None, force: bool = False) -> None:
    domains = DOMAIN_TYPES[:] if domains is None else domains
    problem_ids = _normalize_problem_ids(problems)

    for domain_name in domains:
        source_dir = Path("ipc2023-dataset-main/opt") / domain_name
        target_dir = Path("materials") / domain_name
        target_dir.mkdir(parents=True, exist_ok=True)

        domain_target = target_dir / "domain.pddl"
        if force or not domain_target.exists():
            shutil.copy(source_dir / "domain.pddl", domain_target)

        for problem_id in problem_ids:
            problem_dir = target_dir / problem_id
            problem_dir.mkdir(parents=True, exist_ok=True)

            for suffix in ("pddl", "plan"):
                source_path = source_dir / f"{problem_id}.{suffix}"
                target_path = problem_dir / f"{problem_id}.{suffix}"
                if force or not target_path.exists():
                    shutil.copy(source_path, target_path)


def process_domains(
    domains: list[str] | None = None,
    problems: list[str] | None = None,
    force: bool = False,
    shuffle_seed: int = 52,
) -> None:
    domains = DOMAIN_TYPES[:] if domains is None else domains
    problem_ids = _normalize_problem_ids(problems)

    for domain_name in domains:
        domain_dir = Path("materials") / domain_name
        domain_path = domain_dir / "domain.pddl"

        for problem_id in problem_ids:
            problem_dir = domain_dir / problem_id
            if force:
                _cleanup_problem_variants(problem_dir)
                shuffle_meta_path = problem_dir / "shuffle_meta.json"
                if shuffle_meta_path.exists():
                    shuffle_meta_path.unlink()

            if not force and _variants_are_up_to_date(problem_dir):
                continue

            shuffle(
                domain_path=domain_path,
                problem_path=problem_dir / f"{problem_id}.pddl",
                optimal_plan_path=problem_dir / f"{problem_id}.plan",
                save_dir=problem_dir,
                seed=shuffle_seed,
                problem_id=problem_id,
            )
