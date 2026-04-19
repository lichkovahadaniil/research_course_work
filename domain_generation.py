import shutil
from pathlib import Path

from shuffler import shuffle


DOMAIN_TYPES = ["folding", "labyrinth", "recharging-robots", "ricochet-robots", "rubiks-cube"]


def _normalize_problem_ids(problems: list[str] | None) -> list[str]:
    if problems is None:
        return [f"p{i:02d}" for i in range(1, 21)]
    return sorted(set(problems))


def generate_paths(domains: list[str], problems: list[str] | None = None, force: bool = False) -> None:
    problem_ids = _normalize_problem_ids(problems)

    for domain_name in domains:
        src_path = Path(f"ipc2023-dataset-main/opt/{domain_name}")
        dest_path = Path(f"materials/{domain_name}")

        dest_path.mkdir(parents=True, exist_ok=True)

        domain_dest = dest_path / "domain.pddl"
        if force or not domain_dest.exists():
            shutil.copy(src_path / "domain.pddl", domain_dest)

        for problem_id in problem_ids:
            subfolder = dest_path / problem_id
            subfolder.mkdir(exist_ok=True)

            problem_dest = subfolder / f"{problem_id}.pddl"
            plan_dest = subfolder / f"{problem_id}.plan"

            if force or not problem_dest.exists():
                shutil.copy(src_path / f"{problem_id}.pddl", problem_dest)

            if force or not plan_dest.exists():
                shutil.copy(src_path / f"{problem_id}.plan", plan_dest)


def process_domains(
    domains: list[str],
    problems: list[str] | None = None,
    force: bool = False,
    shuffle_seed: int = 52,
    sampling_profile: list[str] | None = None,
    variant_generation_version: str = "v2",
) -> None:
    problem_ids = _normalize_problem_ids(problems)
    sampling_profile = sampling_profile or problem_ids

    total_problems = len(domains) * len(problem_ids)
    processed = 0
    skipped = 0

    for domain_name in domains:
        src_path = Path(f"materials/{domain_name}")
        domain_file = src_path / "domain.pddl"

        print(f"\nPreparing domain {domain_name} ({len(problem_ids)} problems)")

        for problem_id in problem_ids:
            problem_file = src_path / problem_id / f"{problem_id}.pddl"
            optimal_plan_file = src_path / problem_id / f"{problem_id}.plan"
            shuffle_path = src_path / problem_id

            already_shuffled = (shuffle_path / "canonical").exists()
            if already_shuffled and not force:
                print(f"  skip {problem_id}: shuffle variants already exist")
                skipped += 1
                continue

            if already_shuffled and force:
                print(f"  rebuild {problem_id}: regenerating shuffle variants")
            else:
                print(f"  build {problem_id}: generating shuffle variants")

            shuffle(
                domain_file,
                problem_file,
                optimal_plan_file,
                shuffle_path,
                seed=shuffle_seed,
                problem_id=problem_id,
                sampling_profile=sampling_profile,
                variant_generation_version=variant_generation_version,
            )
            processed += 1

    print(f"\n{'=' * 80}")
    print("prepare finished")
    print(f"  processed: {processed}")
    print(f"  skipped:   {skipped}")
    print(f"  total:     {total_problems}")
