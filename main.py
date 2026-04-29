import argparse
import concurrent.futures
import subprocess
import sys
from pathlib import Path

from domain_generation import generate_paths, process_domains
from experiment_config import DOMAIN_TYPES, MODEL_NAMES, PROBLEM_IDS, PROBLEM_REFS, TASK_NAMES, ProblemRef
from manual_model_run import model_output_dir_name
from shuffler import VARIANT_NAMES

DEFAULT_DOMAIN = DOMAIN_TYPES[0]


def normalize_problem_id(problem_id: str) -> str:
    token = problem_id.strip()
    if not token:
        raise ValueError("problem id cannot be empty")
    if token.startswith("p"):
        token = token[1:]
    normalized = f"p{int(token)}"
    if normalized not in PROBLEM_IDS:
        raise ValueError(f"unknown problem id: {problem_id}")
    return normalized


def normalize_problem_refs(tokens: list[str] | None) -> list[ProblemRef]:
    if not tokens:
        return PROBLEM_REFS[:]

    selected: list[ProblemRef] = []
    current_task: str | None = None
    current_task_problem_count = 0

    def add_all_for_current_task() -> None:
        if current_task is None:
            return
        selected.extend(ProblemRef(current_task, problem_id) for problem_id in PROBLEM_IDS)

    for raw_token in tokens:
        token = raw_token.strip().lower()
        if not token:
            continue

        if token in TASK_NAMES:
            if current_task is not None and current_task_problem_count == 0:
                add_all_for_current_task()
            current_task = token
            current_task_problem_count = 0
            continue

        if current_task is None:
            raise ValueError(
                f"problem id '{raw_token}' must follow a task name: "
                f"{', '.join(TASK_NAMES)}"
            )
        selected.append(ProblemRef(current_task, normalize_problem_id(token)))
        current_task_problem_count += 1

    if current_task is not None and current_task_problem_count == 0:
        add_all_for_current_task()

    deduplicated: list[ProblemRef] = []
    seen: set[ProblemRef] = set()
    for problem_ref in selected:
        if problem_ref in seen:
            continue
        deduplicated.append(problem_ref)
        seen.add(problem_ref)
    return deduplicated


def normalize_problem_ids(tokens: list[str] | None) -> list[ProblemRef]:
    return normalize_problem_refs(tokens)


def build_run_commands(
    problem_refs: list[ProblemRef],
    models: list[str],
    orders: list[str],
    runs: int,
    force: bool,
) -> list[list[str]]:
    if runs < 1:
        raise ValueError("runs must be at least 1")

    commands: list[list[str]] = []
    script_path = Path(__file__).with_name("manual_model_run.py")

    for problem_ref in problem_refs:
        problem_dir = Path("materials") / DEFAULT_DOMAIN / problem_ref.task / problem_ref.problem
        problem_path = problem_dir / f"{problem_ref.problem}.pddl"
        optimal_plan_path = problem_dir / f"{problem_ref.problem}.plan"

        for order_name in orders:
            order_dir = problem_dir / order_name
            domain_path = order_dir / "domain.pddl"
            if not domain_path.exists():
                raise FileNotFoundError(
                    f"missing variant domain: {domain_path}. Run `python3 main.py --force` first."
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
    problem_refs: list[ProblemRef],
    models: list[str],
    orders: list[str],
    runs: int,
    jobs: int = 1,
    force: bool = False,
) -> None:
    commands = build_run_commands(problem_refs, models, orders, runs, force)
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
    generate_paths(DOMAIN_TYPES, PROBLEM_REFS, force=force)
    process_domains(DOMAIN_TYPES, PROBLEM_REFS, force=force)


def report() -> None:
    from plot_metrics import build_reports

    build_reports(DOMAIN_TYPES, PROBLEM_REFS)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Minimal planning pipeline.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="When no command is supplied, run the prepare step with force enabled.",
    )
    subparsers = parser.add_subparsers(dest="command")

    prepare_parser = subparsers.add_parser("prepare", help="Prepare materials and domain variants.")
    prepare_parser.add_argument("--force", action="store_true")

    models_run_parser = subparsers.add_parser("models-run", help="Run all requested model jobs.")
    models_run_parser.add_argument("--models", nargs="+", choices=MODEL_NAMES, required=True)
    models_run_parser.add_argument(
        "--problems",
        nargs="*",
        metavar="PROBLEM_SELECTION",
        help="Task-scoped problem list, e.g. `alpha p1 p2`; task alone selects all p1-p20.",
    )
    models_run_parser.add_argument("--orders", nargs="+", choices=VARIANT_NAMES, required=True)
    models_run_parser.add_argument("--runs", type=int, default=1)
    models_run_parser.add_argument("--jobs", type=int, default=1, help="Number of parallel processes (default: 1)")
    models_run_parser.add_argument("--force", action="store_true")

    subparsers.add_parser("report", help="Build barplot reports.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        prepare_with_force(force=args.force)
        return

    if args.command == "prepare":
        prepare_with_force(force=args.force)
        return

    if args.command == "models-run":
        if args.runs < 1:
            parser.error("--runs must be at least 1")
        try:
            problem_refs = normalize_problem_refs(args.problems)
        except ValueError as exc:
            parser.error(str(exc))
        run_models(
            problem_refs,
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
