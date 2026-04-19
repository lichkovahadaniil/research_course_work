import argparse
import json
import shlex
from datetime import datetime
from pathlib import Path
import time
from typing import Any

from checker import build_metrics
from domain_generation import DOMAIN_TYPES, generate_paths, process_domains
from result_backfill import fill_missing_runtime_fields, load_json_dict, result_payload_is_complete


DEFAULT_PROBLEM_PROFILE = ["p01", "p05", "p10", "p15", "p20"]
DEFAULT_MODELS = [
    "openai/gpt-5-mini",
    "x-ai/grok-4.1-fast",
    "xiaomi/mimo-v2-flash",
    "qwen/qwen3.5-35b-a3b:alibaba",
]


def parse_csv_argument(raw_value: str | None, default: list[str]) -> list[str]:
    if raw_value is None:
        return default[:]
    return [item.strip() for item in raw_value.split(",") if item.strip()]


def normalize_problem_id(problem_id: str) -> str:
    token = problem_id.strip()
    if not token:
        raise ValueError("problem id cannot be empty")
    if token.startswith("p") and len(token) == 3:
        return token
    if token.startswith("p"):
        token = token[1:]
    return f"p{int(token):02d}"


def parse_problem_argument(raw_value: str | None, default: list[str]) -> list[str]:
    values = parse_csv_argument(raw_value, default)
    return [normalize_problem_id(value) for value in values]


def model_output_dir_name(model_name: str) -> str:
    return model_name.split("/")[-1].replace(":", "-").replace(".", "-")


def load_json(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, payload: dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def iter_problem_dirs(domain_name: str, problem_ids: list[str]) -> list[Path]:
    domain_path = Path("materials") / domain_name
    return [domain_path / problem_id for problem_id in problem_ids if (domain_path / problem_id).is_dir()]


def iter_variant_dirs(problem_dir: Path, variants: list[str] | None = None) -> list[Path]:
    if variants is None or variants == ["all"]:
        return sorted(
            child for child in problem_dir.iterdir()
            if child.is_dir() and (child / "domain.pddl").exists()
        )

    requested = []
    for variant_name in variants:
        candidate = problem_dir / variant_name
        if candidate.is_dir() and (candidate / "domain.pddl").exists():
            requested.append(candidate)
    return requested


def build_variant_summary(variant_dir: Path) -> dict[str, Any]:
    strict_summary: dict[str, Any] = {}
    legacy_summary: dict[str, Any] = {}
    order_summary: dict[str, Any] = {}
    results_by_model: dict[str, Any] = {}

    for model_dir in sorted(child for child in variant_dir.iterdir() if child.is_dir()):
        result_path = model_dir / "llm_result.json"
        plan_path = model_dir / "llm.plan"
        if not result_path.exists() or not plan_path.exists():
            continue

        entry = load_json(result_path)
        metrics = entry.get("metrics", {})
        strict = metrics.get("strict") or {}
        legacy = metrics.get("legacy") or {}
        order = metrics.get("order") or {}

        strict_summary[model_dir.name] = {
            "parsable": strict.get("parsable"),
            "plan_length": strict.get("plan_length"),
            "executability": strict.get("executability"),
            "reachability": strict.get("reachability"),
            "first_failure_step": strict.get("first_failure_step"),
            "non_executable_failure": strict.get("non_executable_failure"),
            "strict_final_value": strict.get("strict_final_value"),
        }
        legacy_summary[model_dir.name] = {
            "cost": legacy.get("cost"),
            "gap": legacy.get("gap"),
            "bug_optimal": legacy.get("bug_optimal"),
            "optimality_ratio": legacy.get("optimality_ratio"),
            "optimal_cost": (metrics.get("reference") or {}).get("optimal_cost"),
        }
        order_summary[model_dir.name] = order

        results_by_model[model_dir.name] = {
            "model": entry.get("model"),
            "plan_file": entry.get("plan_file"),
            "duration_sec": entry.get("duration_sec"),
            "prompt_tokens": entry.get("prompt_tokens"),
            "completion_tokens": entry.get("completion_tokens"),
            "total_tokens": entry.get("total_tokens"),
            "reasoning_enabled": entry.get("reasoning_enabled"),
            "metrics": metrics,
        }

    summary = {
        "problem": variant_dir.parent.name,
        "variant": variant_dir.name,
        "strict_summary": strict_summary,
        "legacy_summary": legacy_summary,
        "order_summary": order_summary,
    }
    save_json(variant_dir / "llm_summary.json", summary)

    metrics_payload = {
        "problem": variant_dir.parent.name,
        "variant": variant_dir.name,
        "results_by_model": results_by_model,
    }
    save_json(variant_dir / "llm_metrics.json", metrics_payload)

    return summary


def build_global_metrics(domains: list[str], problem_ids: list[str] | None = None) -> dict[str, Any]:
    metric_path = Path("materials/metric.json")
    global_metric: dict[str, Any] = {}

    if metric_path.exists():
        try:
            global_metric = load_json(metric_path)
        except json.JSONDecodeError:
            global_metric = {}

    meta = global_metric.get("_meta", {}) if isinstance(global_metric.get("_meta"), dict) else {}
    domain_meta = meta.get("domains", {}) if isinstance(meta.get("domains"), dict) else {}
    selected_problem_ids = set(problem_ids) if problem_ids is not None else None

    for domain_name in domains:
        domain_metric: dict[str, Any] = {}
        domain_path = Path("materials") / domain_name
        for problem_dir in sorted(child for child in domain_path.glob("p*") if child.is_dir()):
            if selected_problem_ids is not None and problem_dir.name not in selected_problem_ids:
                continue
            problem_metric: dict[str, Any] = {}
            for variant_dir in iter_variant_dirs(problem_dir):
                summary_path = variant_dir / "llm_summary.json"
                if summary_path.exists():
                    problem_metric[variant_dir.name] = load_json(summary_path)
            if problem_metric:
                domain_metric[problem_dir.name] = problem_metric
        global_metric[domain_name] = domain_metric
        domain_meta[domain_name] = {
            "selected_problems": sorted(domain_metric),
            "updated_at": datetime.now().isoformat(),
        }

    global_metric["_meta"] = {
        "domains": domain_meta,
        "updated_at": datetime.now().isoformat(),
    }

    save_json(metric_path, global_metric)
    return global_metric


def safe_build_metrics(
    domain_file: Path,
    problem_file: Path,
    plan_path: Path,
    optimal_plan_path: Path,
) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    try:
        return build_metrics(domain_file, problem_file, plan_path, optimal_plan_path), None
    except Exception as exc:
        return None, {
            "type": type(exc).__name__,
            "message": str(exc),
        }


def build_local_result_entry(
    *,
    model_dir: Path,
    variant_dir: Path,
    plan_path: Path,
    domain_file: Path,
    problem_file: Path,
    optimal_plan_path: Path,
    existing_payload: dict[str, Any] | None,
) -> dict[str, Any]:
    metrics, postprocess_error = safe_build_metrics(domain_file, problem_file, plan_path, optimal_plan_path)
    updated_entry = {
        **(existing_payload or {}),
        "model": (existing_payload or {}).get("model") or model_dir.name,
        "plan_file": str(plan_path),
        "metrics": metrics,
    }
    if postprocess_error is not None:
        updated_entry["postprocess_error"] = postprocess_error
    updated_entry = fill_missing_runtime_fields(
        updated_entry,
        variant_dir=variant_dir,
        model_dir_name=model_dir.name,
    )
    return updated_entry


def aggregate_domains(domains: list[str], problem_ids: list[str], variants: list[str] | None = None) -> None:
    for domain_name in domains:
        for problem_dir in iter_problem_dirs(domain_name, problem_ids):
            problem_file = problem_dir / f"{problem_dir.name}.pddl"
            optimal_plan_path = problem_dir / f"{problem_dir.name}.plan"

            for variant_dir in iter_variant_dirs(problem_dir, variants=variants):
                domain_file = variant_dir / "domain.pddl"
                updated_models = 0
                model_dirs = sorted(child for child in variant_dir.iterdir() if child.is_dir())
                print(f"start aggregate {domain_name}/{problem_dir.name}/{variant_dir.name}: {len(model_dirs)} model(s)")

                for index, model_dir in enumerate(model_dirs, start=1):
                    plan_path = model_dir / "llm.plan"
                    if not plan_path.exists():
                        print(f"  [{index}/{len(model_dirs)}] skip {model_dir.name}: no llm.plan")
                        continue

                    result_path = model_dir / "llm_result.json"
                    existing = load_json_dict(result_path)
                    print(f"  [{index}/{len(model_dirs)}] recompute {model_dir.name}")
                    started_at = time.time()
                    updated_entry = build_local_result_entry(
                        model_dir=model_dir,
                        variant_dir=variant_dir,
                        plan_path=plan_path,
                        domain_file=domain_file,
                        problem_file=problem_file,
                        optimal_plan_path=optimal_plan_path,
                        existing_payload=existing,
                    )
                    save_json(result_path, updated_entry)
                    updated_models += 1
                    print(f"  [{index}/{len(model_dirs)}] done {model_dir.name} in {time.time() - started_at:.1f}s")

                build_variant_summary(variant_dir)
                print(f"aggregated {domain_name}/{problem_dir.name}/{variant_dir.name}: {updated_models} model(s)")

    build_global_metrics(domains, problem_ids=problem_ids)
    print("aggregate finished")


def repair_results(domains: list[str], problem_ids: list[str], variants: list[str] | None = None) -> None:
    repaired_models = 0

    for domain_name in domains:
        for problem_dir in iter_problem_dirs(domain_name, problem_ids):
            problem_file = problem_dir / f"{problem_dir.name}.pddl"
            optimal_plan_path = problem_dir / f"{problem_dir.name}.plan"

            for variant_dir in iter_variant_dirs(problem_dir, variants=variants):
                domain_file = variant_dir / "domain.pddl"
                model_dirs = sorted(child for child in variant_dir.iterdir() if child.is_dir())
                touched_variant = False
                print(f"start repair {domain_name}/{problem_dir.name}/{variant_dir.name}: {len(model_dirs)} model(s)")

                for index, model_dir in enumerate(model_dirs, start=1):
                    plan_path = model_dir / "llm.plan"
                    if not plan_path.exists():
                        print(f"  [{index}/{len(model_dirs)}] skip {model_dir.name}: no llm.plan")
                        continue

                    result_path = model_dir / "llm_result.json"
                    existing = load_json_dict(result_path)
                    if result_payload_is_complete(existing):
                        print(f"  [{index}/{len(model_dirs)}] skip {model_dir.name}: result complete")
                        continue

                    print(f"  [{index}/{len(model_dirs)}] repair {model_dir.name}")
                    started_at = time.time()
                    updated_entry = build_local_result_entry(
                        model_dir=model_dir,
                        variant_dir=variant_dir,
                        plan_path=plan_path,
                        domain_file=domain_file,
                        problem_file=problem_file,
                        optimal_plan_path=optimal_plan_path,
                        existing_payload=existing,
                    )
                    save_json(result_path, updated_entry)
                    repaired_models += 1
                    touched_variant = True
                    print(f"  [{index}/{len(model_dirs)}] done {model_dir.name} in {time.time() - started_at:.1f}s")

                if touched_variant:
                    build_variant_summary(variant_dir)
                    print(f"repaired {domain_name}/{problem_dir.name}/{variant_dir.name}")

    build_global_metrics(domains, problem_ids=problem_ids)
    print(f"repair finished: {repaired_models} model result(s) updated")


def collect_manual_run_commands(
    domains: list[str],
    problem_ids: list[str],
    variants: list[str] | None,
    models: list[str],
) -> list[str]:
    commands: list[str] = []

    for domain_name in domains:
        for problem_dir in iter_problem_dirs(domain_name, problem_ids):
            problem_file = problem_dir / f"{problem_dir.name}.pddl"
            optimal_plan_path = problem_dir / f"{problem_dir.name}.plan"

            for variant_dir in iter_variant_dirs(problem_dir, variants=variants):
                domain_file = variant_dir / "domain.pddl"
                for model_name in models:
                    command = " ".join(
                        [
                            "python3",
                            "manual_model_run.py",
                            "--domain-path",
                            shlex.quote(str(domain_file)),
                            "--problem-path",
                            shlex.quote(str(problem_file)),
                            "--optimal-plan-path",
                            shlex.quote(str(optimal_plan_path)),
                            "--variant-dir",
                            shlex.quote(str(variant_dir)),
                            "--model",
                            shlex.quote(model_name),
                        ]
                    )
                    commands.append(command)

    return commands


def print_run_commands(domains: list[str], problem_ids: list[str], variants: list[str] | None, models: list[str]) -> None:
    for command in collect_manual_run_commands(domains, problem_ids, variants, models):
        print(command)


def prepare_domains(domains: list[str], problem_ids: list[str], force: bool, shuffle_seed: int) -> None:
    generate_paths(domains, problems=problem_ids, force=force)
    process_domains(
        domains,
        problems=problem_ids,
        force=force,
        shuffle_seed=shuffle_seed,
        sampling_profile=problem_ids,
    )


def report_domains(domains: list[str], problem_ids: list[str] | None = None) -> None:
    from plot_folding_metrics import build_reports_for_domains

    build_reports_for_domains(domains, problem_ids=problem_ids)
    print("report finished")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manual-first LLM planning pipeline. No model calls are made unless you run the printed commands yourself."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser("prepare", help="Copy problems and generate shuffled domain variants.")
    prepare_parser.add_argument("--domains", type=str, default=",".join(DOMAIN_TYPES))
    prepare_parser.add_argument("--problems", type=str, default=",".join(DEFAULT_PROBLEM_PROFILE))
    prepare_parser.add_argument("--force", action="store_true")
    prepare_parser.add_argument("--shuffle-seed", type=int, default=52)

    print_parser = subparsers.add_parser("print-run-commands", help="Print manual model-run commands without executing them.")
    print_parser.add_argument("--domains", type=str, default=",".join(DOMAIN_TYPES))
    print_parser.add_argument("--problems", type=str, default=",".join(DEFAULT_PROBLEM_PROFILE))
    print_parser.add_argument("--variants", type=str, default="all")
    print_parser.add_argument("--models", type=str, default=",".join(DEFAULT_MODELS))

    aggregate_parser = subparsers.add_parser("aggregate", help="Recompute local metrics from existing plans only.")
    aggregate_parser.add_argument("--domains", type=str, default=",".join(DOMAIN_TYPES))
    aggregate_parser.add_argument("--problems", type=str, default=",".join(DEFAULT_PROBLEM_PROFILE))
    aggregate_parser.add_argument("--variants", type=str, default="all")

    repair_parser = subparsers.add_parser("repair-results", help="Only rebuild missing or incomplete llm_result.json files from existing plans.")
    repair_parser.add_argument("--domains", type=str, default=",".join(DOMAIN_TYPES))
    repair_parser.add_argument("--problems", type=str, default=",".join(DEFAULT_PROBLEM_PROFILE))
    repair_parser.add_argument("--variants", type=str, default="all")

    report_parser = subparsers.add_parser("report", help="Build plots and report artifacts from aggregated metrics.")
    report_parser.add_argument("--domains", type=str, default=",".join(DOMAIN_TYPES))
    report_parser.add_argument("--problems", type=str, default=None)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    domains = parse_csv_argument(args.domains, DOMAIN_TYPES)

    if args.command == "prepare":
        problem_ids = parse_problem_argument(args.problems, DEFAULT_PROBLEM_PROFILE)
        prepare_domains(domains, problem_ids, force=args.force, shuffle_seed=args.shuffle_seed)
        return

    if args.command == "print-run-commands":
        problem_ids = parse_problem_argument(args.problems, DEFAULT_PROBLEM_PROFILE)
        variants = parse_csv_argument(args.variants, ["all"])
        models = parse_csv_argument(args.models, DEFAULT_MODELS)
        print_run_commands(domains, problem_ids, variants, models)
        return

    if args.command == "aggregate":
        problem_ids = parse_problem_argument(args.problems, DEFAULT_PROBLEM_PROFILE)
        variants = parse_csv_argument(args.variants, ["all"])
        aggregate_domains(domains, problem_ids, variants=variants)
        return

    if args.command == "repair-results":
        problem_ids = parse_problem_argument(args.problems, DEFAULT_PROBLEM_PROFILE)
        variants = parse_csv_argument(args.variants, ["all"])
        repair_results(domains, problem_ids, variants=variants)
        return

    if args.command == "report":
        problem_ids = None if args.problems is None else parse_problem_argument(args.problems, DEFAULT_PROBLEM_PROFILE)
        report_domains(domains, problem_ids=problem_ids)
        return


if __name__ == "__main__":
    main()
