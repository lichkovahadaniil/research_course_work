import argparse
import subprocess
import sys
from pathlib import Path
import concurrent.futures

from domain_generation import DOMAIN_TYPES, PROBLEM_IDS, generate_paths, process_domains
from shuffler import VARIANT_NAMES


MODEL_NAMES = [
    "gpt-5-mini",
    "grok-4.1-fast",
    "qwen/qwen3.5-35b-a3b:alibaba",
]


def normalize_problem_id(problem_id: str) -> str:
    token = problem_id.strip()
    if not token:
        raise ValueError("problem id cannot be empty")
    if token.startswith("p"):
        token = token[1:]
    return f"p{int(token):02d}"


def normalize_problem_ids(problem_ids: list[str] | None) -> list[str]:
    if not problem_ids:
        return PROBLEM_IDS[:]
    return [normalize_problem_id(problem_id) for problem_id in problem_ids]


def build_run_commands(domains: list[str], problem_ids: list[str]) -> list[list[str]]:
    commands: list[list[str]] = []
    script_path = Path(__file__).with_name("manual_model_run.py")

    for domain_name in domains:
        for problem_id in problem_ids:
            problem_dir = Path("materials") / domain_name / problem_id
            problem_path = problem_dir / f"{problem_id}.pddl"
            optimal_plan_path = problem_dir / f"{problem_id}.plan"

            for variant_name in VARIANT_NAMES:
                variant_dir = problem_dir / variant_name
                domain_path = variant_dir / "domain.pddl"
                if not domain_path.exists():
                    raise FileNotFoundError(
                        f"missing variant domain: {domain_path}. Run `python3 main.py prepare --force` first."
                    )

                for model_name in MODEL_NAMES:
                    commands.append(
                        [
                            sys.executable,
                            str(script_path),
                            "--domain-path",
                            str(domain_path),
                            "--problem-path",
                            str(problem_path),
                            "--optimal-plan-path",
                            str(optimal_plan_path),
                            "--variant-dir",
                            str(variant_dir),
                            "--model",
                            model_name,
                        ]
                    )
    return commands


def run_models(domains: list[str], problem_ids: list[str], jobs: int = 1) -> None:
    commands = build_run_commands(domains, problem_ids)
    total = len(commands)

    if jobs == 1:
        for index, command in enumerate(commands, start=1):
            subprocess.run(command, check=True)
            print(f"[{index}/{total}] {' '.join(command[1:])}")
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=jobs) as executor:
            future_to_cmd = {
                executor.submit(subprocess.run, cmd, check=True): cmd
                for cmd in commands
            }
            for index, future in enumerate(concurrent.futures.as_completed(future_to_cmd), start=1):
                cmd = future_to_cmd[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"[{index}/{total}] ✗ {' '.join(cmd[1:])} → {e}")


def prepare_with_force(force: bool) -> None:
    generate_paths(DOMAIN_TYPES, PROBLEM_IDS, force=force)
    process_domains(DOMAIN_TYPES, PROBLEM_IDS, force=force)


def report() -> None:
    from plot_metrics import build_reports

    build_reports(DOMAIN_TYPES, PROBLEM_IDS)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Minimal planning pipeline.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser("prepare", help="Prepare materials and domain variants.")
    prepare_parser.add_argument("--force", action="store_true")

    models_run_parser = subparsers.add_parser("models-run", help="Run all requested model jobs.")
    models_run_parser.add_argument("--domain", choices=DOMAIN_TYPES)
    models_run_parser.add_argument("--problems", nargs="*")
    models_run_parser.add_argument("--all", action="store_true")
    models_run_parser.add_argument("--jobs", type=int, default=1, help="Number of parallel processes (default: 1)")

    subparsers.add_parser("report", help="Build barplot reports.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "prepare":
        prepare_with_force(force=args.force)
        return

    if args.command == "models-run":
        if args.all:
            run_models(DOMAIN_TYPES, PROBLEM_IDS, jobs=args.jobs)
            return
        if args.domain is None:
            parser.error("--domain is required unless --all is used")
        run_models([args.domain], normalize_problem_ids(args.problems), jobs=args.jobs)
        return

    if args.command == "report":
        report()
        return


if __name__ == "__main__":
    main()
