import shutil
from pathlib import Path

from shuffler import VARIANT_NAMES, shuffle


DOMAIN_TYPES = ["folding", "labyrinth"]
PROBLEM_IDS = [f"p{index:02d}" for index in range(1, 21)]


def _normalize_problem_ids(problems: list[str] | None = None) -> list[str]:
    return PROBLEM_IDS[:] if problems is None else sorted(set(problems))


def _cleanup_problem_variants(problem_dir: Path) -> None:
    for child in problem_dir.iterdir():
        if not child.is_dir():
            continue
        if child.name in VARIANT_NAMES or (child / "domain.pddl").exists():
            shutil.rmtree(child)


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

            frequency_dir = problem_dir / "frequency"
            if frequency_dir.exists() and not force:
                continue

            shuffle(
                domain_path=domain_path,
                problem_path=problem_dir / f"{problem_id}.pddl",
                optimal_plan_path=problem_dir / f"{problem_id}.plan",
                save_dir=problem_dir,
                seed=shuffle_seed,
                problem_id=problem_id,
            )
