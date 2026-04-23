import argparse
import concurrent.futures
import subprocess
import sys
from pathlib import Path

from domain_generation import generate_paths, process_domains
from experiment_config import DOMAIN_TYPES, MODEL_NAMES, PROBLEM_IDS
from manual_model_run import model_output_dir_name
from shuffler import VARIANT_NAMES

DEFAULT_DOMAIN = DOMAIN_TYPES[0]


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


def build_run_commands(
    problem_ids: list[str],
    models: list[str],
    orders: list[str],
    runs: int,
    force: bool,
) -> list[list[str]]:
    if runs < 1:
        raise ValueError("runs must be at least 1")

    commands: list[list[str]] = []
    script_path = Path(__file__).with_name("manual_model_run.py")

    for problem_id in problem_ids:
        problem_dir = Path("materials") / DEFAULT_DOMAIN / problem_id
        problem_path = problem_dir / f"{problem_id}.pddl"
        optimal_plan_path = problem_dir / f"{problem_id}.plan"

        for order_name in orders:
            order_dir = problem_dir / order_name
            domain_path = order_dir / "domain.pddl"
            if not domain_path.exists():
                raise FileNotFoundError(
                    f"missing variant domain: {domain_path}. Run `python3 main.py prepare --force` first."
                )

            for run_id in range(1, runs + 1):
                run_dir = order_dir / str(run_id)

                for model_name in models:
                    output_dir = run_dir / model_output_dir_name(model_name)
                    plan_path = output_dir / "llm.plan"
                    if plan_path.exists() and not force:
                        continue

                    command = [
                        sys.executable,
                        str(script_path),
                        "--domain-path",
                        str(domain_path),
                        "--problem-path",
                        str(problem_path),
                        "--optimal-plan-path",
                        str(optimal_plan_path),
                        "--output-dir",
                        str(output_dir),
                        "--model",
                        model_name,
                    ]
                    if force:
                        command.append("--force")
                    commands.append(command)
    return commands


def run_models(
    problem_ids: list[str],
    models: list[str],
    orders: list[str],
    runs: int,
    jobs: int = 1,
    force: bool = False,
) -> None:
    commands = build_run_commands(problem_ids, models, orders, runs, force)
    total = len(commands)
    if total == 0:
        print("Nothing to run.")
        return

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
    models_run_parser.add_argument("--models", nargs="+", choices=MODEL_NAMES, required=True)
    models_run_parser.add_argument("--problems", nargs="*")
    models_run_parser.add_argument("--orders", nargs="+", choices=VARIANT_NAMES, required=True)
    models_run_parser.add_argument("--runs", type=int, default=1)
    models_run_parser.add_argument("--jobs", type=int, default=1, help="Number of parallel processes (default: 1)")
    models_run_parser.add_argument("--force", action="store_true")

    subparsers.add_parser("report", help="Build barplot reports.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "prepare":
        prepare_with_force(force=args.force)
        return

    if args.command == "models-run":
        if args.runs < 1:
            parser.error("--runs must be at least 1")
        run_models(
            normalize_problem_ids(args.problems),
            args.models,
            args.orders,
            args.runs,
            jobs=args.jobs,
            force=args.force,
        )
        return

    if args.command == "report":
        report()
        return


if __name__ == "__main__":
    main()
