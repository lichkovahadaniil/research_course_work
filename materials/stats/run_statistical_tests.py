import csv
import json
import math
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from experiment_config import MODEL_NAMES, PROBLEM_IDS
from manual_model_run import model_output_dir_name
from shuffler import VARIANT_NAMES
from token_usage import build_token_usage_from_payload


BASELINE_ORDER = "canonical"
COMPARED_ORDERS = [order for order in VARIANT_NAMES if order != BASELINE_ORDER]
DATA_ROOT = PROJECT_ROOT / "materials" / "logistics" / "alpha"
OUTPUT_DIR = Path(__file__).resolve().parent

BINARY_METRICS = {
    "reachability": "Goal reached under strict VAL validation.",
    "executability": "Plan executed under strict VAL validation.",
    "non_executable_failure": "Strict validation failed before executable completion.",
}
CONDITIONAL_BINARY_METRICS = {
    "conditional_reachability": (
        "Goal reached among pairs where both orders produced executable plans."
    ),
}
NUMERIC_METRICS = {
    "plan_length": "Strict VAL plan length; only available when goal is reached.",
    "optimality_ratio": "Validated cost divided by reference cost; only available when goal is reached.",
    "first_failure_step": "First failed execution step; only available for state execution errors.",
    "prompt_tokens": "Prompt tokens reported by provider.",
    "completion_tokens": "Completion tokens reported or normalized from provider payload.",
    "reasoning_completion_tokens": "Reasoning-token component of completion tokens.",
    "raw_completion_tokens": "Raw answer-token component of completion tokens.",
    "total_tokens": "Total tokens reported or normalized from provider payload.",
    "duration_sec": "Model call duration in seconds.",
}


def exact_mcnemar_p(order_only: int, baseline_only: int) -> float:
    discordant = order_only + baseline_only
    if discordant == 0:
        return 1.0
    tail = sum(
        math.comb(discordant, k)
        for k in range(0, min(order_only, baseline_only) + 1)
    ) / (2**discordant)
    return min(1.0, 2.0 * tail)


def t_pdf(x: float, df: int) -> float:
    return math.exp(
        math.lgamma((df + 1) / 2)
        - math.lgamma(df / 2)
        - 0.5 * math.log(df * math.pi)
        - ((df + 1) / 2) * math.log1p((x * x) / df)
    )


def simpson_integral(func, lower: float, upper: float, intervals: int = 12000) -> float:
    if lower == upper:
        return 0.0
    if intervals % 2:
        intervals += 1
    step = (upper - lower) / intervals
    total = func(lower) + func(upper)
    for index in range(1, intervals):
        total += (4 if index % 2 else 2) * func(lower + index * step)
    return total * step / 3


def t_cdf(value: float, df: int) -> float:
    if value == 0:
        return 0.5
    area = simpson_integral(lambda x: t_pdf(x, df), 0.0, abs(value))
    return 0.5 + area if value > 0 else 0.5 - area


def paired_t_test(differences: list[float]) -> dict[str, float | int | None]:
    sample_size = len(differences)
    if sample_size < 2:
        return {
            "n": sample_size,
            "mean_diff": statistics.mean(differences) if differences else None,
            "sd_diff": None,
            "t": None,
            "df": sample_size - 1,
            "p_value": None,
            "cohens_dz": None,
        }

    mean_diff = statistics.mean(differences)
    sd_diff = statistics.stdev(differences)
    if sd_diff == 0:
        t_value = 0.0 if mean_diff == 0 else math.copysign(math.inf, mean_diff)
        p_value = 1.0 if mean_diff == 0 else 0.0
        cohens_dz = 0.0 if mean_diff == 0 else math.copysign(math.inf, mean_diff)
    else:
        t_value = mean_diff / (sd_diff / math.sqrt(sample_size))
        p_value = 2 * (1 - t_cdf(abs(t_value), sample_size - 1))
        p_value = max(0.0, min(1.0, p_value))
        cohens_dz = mean_diff / sd_diff

    return {
        "n": sample_size,
        "mean_diff": mean_diff,
        "sd_diff": sd_diff,
        "t": t_value,
        "df": sample_size - 1,
        "p_value": p_value,
        "cohens_dz": cohens_dz,
    }


def sign_flip_permutation_p(
    differences: list[float],
    *,
    samples: int = 100000,
    seed: int = 12345,
) -> float | None:
    if not differences:
        return None

    nonzero = [value for value in differences if value != 0]
    if not nonzero:
        return 1.0

    observed = abs(sum(nonzero) / len(differences))
    nonzero_count = len(nonzero)
    if nonzero_count <= 20:
        extreme = 0
        total = 1 << nonzero_count
        for mask in range(total):
            signed_sum = 0.0
            for index, value in enumerate(nonzero):
                signed_sum += value if (mask >> index) & 1 else -value
            if abs(signed_sum / len(differences)) >= observed - 1e-12:
                extreme += 1
        return extreme / total

    rng = random.Random(seed)
    extreme = 0
    for _ in range(samples):
        signed_sum = sum(value if rng.random() < 0.5 else -value for value in nonzero)
        if abs(signed_sum / len(differences)) >= observed - 1e-12:
            extreme += 1
    return extreme / samples


def holm_adjust(results: list[dict[str, Any]], p_key: str) -> list[float | None]:
    indexed = [
        (index, result[p_key])
        for index, result in enumerate(results)
        if result.get(p_key) is not None
    ]
    ordered = sorted(indexed, key=lambda item: item[1])
    adjusted: list[float | None] = [None] * len(results)
    running = 0.0
    total = len(ordered)
    for rank, (index, p_value) in enumerate(ordered):
        value = min(1.0, p_value * (total - rank))
        running = max(running, value)
        adjusted[index] = running
    return adjusted


def load_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for problem_id in PROBLEM_IDS:
        for order_name in VARIANT_NAMES:
            variant_dir = DATA_ROOT / problem_id / order_name
            run_dirs = sorted(
                [
                    child
                    for child in variant_dir.glob("[0-9]*")
                    if child.is_dir() and child.name.isdigit()
                ],
                key=lambda child: int(child.name),
            )
            for run_dir in run_dirs:
                for model_name in MODEL_NAMES:
                    result_path = (
                        run_dir
                        / model_output_dir_name(model_name)
                        / "llm_result.json"
                    )
                    if not result_path.exists():
                        continue
                    payload = json.loads(result_path.read_text(encoding="utf-8"))
                    metrics = payload.get("metrics") or {}
                    strict = metrics.get("strict") or {}
                    legacy = metrics.get("legacy") or {}
                    token_usage = build_token_usage_from_payload(payload)
                    executable = bool(strict.get("executability"))
                    reachable = bool(strict.get("reachability"))
                    rows.append(
                        {
                            "problem": problem_id,
                            "run": int(run_dir.name),
                            "model": model_name,
                            "order": order_name,
                            "reachability": 1.0 if reachable else 0.0,
                            "executability": 1.0 if executable else 0.0,
                            "conditional_reachability": (1.0 if reachable else 0.0)
                            if executable
                            else None,
                            "non_executable_failure": 1.0
                            if strict.get("non_executable_failure") is not None
                            else 0.0,
                            "plan_length": strict.get("plan_length") if reachable else None,
                            "optimality_ratio": legacy.get("optimality_ratio")
                            if reachable
                            else None,
                            "first_failure_step": strict.get("first_failure_step"),
                            "prompt_tokens": token_usage["prompt_tokens"],
                            "completion_tokens": token_usage["completion_tokens"],
                            "reasoning_completion_tokens": token_usage[
                                "reasoning_completion_tokens"
                            ],
                            "raw_completion_tokens": token_usage["raw_completion_tokens"],
                            "total_tokens": token_usage["total_tokens"],
                            "duration_sec": payload.get("duration_sec"),
                        }
                    )
    return rows


def build_pairs(
    rows: list[dict[str, Any]],
    model_name: str,
    metric: str,
    order_name: str,
    *,
    require_both_executable: bool = False,
) -> list[tuple[float, float]]:
    by_key: dict[tuple[str, int], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        if row["model"] != model_name:
            continue
        by_key[(row["problem"], row["run"])][row["order"]] = row

    pairs: list[tuple[float, float]] = []
    for values in by_key.values():
        if BASELINE_ORDER not in values or order_name not in values:
            continue
        baseline = values[BASELINE_ORDER]
        compared = values[order_name]
        if require_both_executable and not (
            baseline["executability"] == 1.0 and compared["executability"] == 1.0
        ):
            continue
        baseline_value = baseline.get(metric)
        compared_value = compared.get(metric)
        if baseline_value is None or compared_value is None:
            continue
        pairs.append((float(baseline_value), float(compared_value)))
    return pairs


def mcnemar_result(
    rows: list[dict[str, Any]],
    model_name: str,
    metric: str,
    order_name: str,
    *,
    require_both_executable: bool = False,
) -> dict[str, Any]:
    pairs = build_pairs(
        rows,
        model_name,
        metric,
        order_name,
        require_both_executable=require_both_executable,
    )
    n00 = n01 = n10 = n11 = 0
    for baseline_value, compared_value in pairs:
        baseline = int(baseline_value)
        compared = int(compared_value)
        if baseline == 0 and compared == 0:
            n00 += 1
        elif baseline == 0 and compared == 1:
            n01 += 1
        elif baseline == 1 and compared == 0:
            n10 += 1
        elif baseline == 1 and compared == 1:
            n11 += 1

    sample_size = n00 + n01 + n10 + n11
    p_value = exact_mcnemar_p(n01, n10)
    return {
        "model": model_name,
        "metric": metric,
        "test": "exact_mcnemar",
        "baseline_order": BASELINE_ORDER,
        "compared_order": order_name,
        "n_pairs": sample_size,
        "n00_both_fail": n00,
        "n01_compared_only_success": n01,
        "n10_baseline_only_success": n10,
        "n11_both_success": n11,
        "baseline_mean": (n10 + n11) / sample_size if sample_size else None,
        "compared_mean": (n01 + n11) / sample_size if sample_size else None,
        "risk_difference": (n01 - n10) / sample_size if sample_size else None,
        "matched_odds_ratio": None if n10 == 0 else n01 / n10,
        "matched_odds_ratio_haldane": (n01 + 0.5) / (n10 + 0.5),
        "p_value": p_value,
        "requires_both_executable": require_both_executable,
    }


def numeric_result(
    rows: list[dict[str, Any]],
    model_name: str,
    metric: str,
    order_name: str,
) -> dict[str, Any]:
    pairs = build_pairs(rows, model_name, metric, order_name)
    baseline_values = [baseline for baseline, _ in pairs]
    compared_values = [compared for _, compared in pairs]
    differences = [compared - baseline for baseline, compared in pairs]
    t_result = paired_t_test(differences)
    permutation_p = sign_flip_permutation_p(differences)
    baseline_mean = statistics.mean(baseline_values) if baseline_values else None
    compared_mean = statistics.mean(compared_values) if compared_values else None
    mean_diff = t_result["mean_diff"]
    return {
        "model": model_name,
        "metric": metric,
        "test": "paired_t_and_sign_flip_permutation",
        "baseline_order": BASELINE_ORDER,
        "compared_order": order_name,
        "n_pairs": len(pairs),
        "baseline_mean": baseline_mean,
        "compared_mean": compared_mean,
        "mean_difference": mean_diff,
        "percent_difference_vs_baseline": (
            mean_diff / baseline_mean
            if mean_diff is not None and baseline_mean not in (None, 0)
            else None
        ),
        "sd_difference": t_result["sd_diff"],
        "t_statistic": t_result["t"],
        "degrees_of_freedom": t_result["df"],
        "p_value_t_test": t_result["p_value"],
        "p_value_sign_flip_permutation": permutation_p,
        "cohens_dz": t_result["cohens_dz"],
    }


def format_number(value: Any, digits: int = 4) -> str:
    if value is None:
        return "NA"
    if isinstance(value, float):
        if math.isnan(value):
            return "NA"
        if math.isinf(value):
            return "inf" if value > 0 else "-inf"
        return f"{value:.{digits}f}"
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def markdown_report(model_name: str, payload: dict[str, Any]) -> str:
    lines = [
        f"# Statistical Tests: {model_name}",
        "",
        "Baseline order: `canonical`.",
        "Compared orders: `disp_1`, `disp_2`, `disp_3`.",
        "",
        "Pairing unit: `(problem, run)` within this model. Each test only uses pairs where both the baseline and compared order have an available value.",
        "",
        "## Binary Metrics",
        "",
        "Exact McNemar test is used for binary outcomes. `b` means compared order succeeds while canonical fails; `c` means canonical succeeds while compared order fails. Effect size is reported as risk difference and matched odds ratio.",
        "",
    ]
    for result in payload["binary_tests"]:
        lines.append(
            "| metric | order | n | canonical | order | b | c | risk diff | matched OR | p | p Holm |"
        )
        break
    if payload["binary_tests"]:
        for result in payload["binary_tests"]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        result["metric"],
                        result["compared_order"],
                        str(result["n_pairs"]),
                        format_number(result["baseline_mean"]),
                        format_number(result["compared_mean"]),
                        str(result["n01_compared_only_success"]),
                        str(result["n10_baseline_only_success"]),
                        format_number(result["risk_difference"]),
                        format_number(result["matched_odds_ratio"]),
                        format_number(result["p_value"], 6),
                        format_number(result["p_value_holm"], 6),
                    ]
                )
                + " |"
            )
    lines.extend(
        [
            "",
            "## Numeric Metrics",
            "",
            "Numeric metrics use paired t-test plus paired sign-flip permutation p-value. Effect size is Cohen's dz: mean paired difference divided by the standard deviation of paired differences.",
            "",
        ]
    )
    if payload["numeric_tests"]:
        lines.append(
            "| metric | order | n | canonical mean | order mean | mean diff | % diff | dz | p t-test | p perm | p perm Holm |"
        )
        for result in payload["numeric_tests"]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        result["metric"],
                        result["compared_order"],
                        str(result["n_pairs"]),
                        format_number(result["baseline_mean"]),
                        format_number(result["compared_mean"]),
                        format_number(result["mean_difference"]),
                        format_number(result["percent_difference_vs_baseline"]),
                        format_number(result["cohens_dz"]),
                        format_number(result["p_value_t_test"], 6),
                        format_number(result["p_value_sign_flip_permutation"], 6),
                        format_number(result["p_value_sign_flip_permutation_holm"], 6),
                    ]
                )
                + " |"
            )
    lines.append("")
    return "\n".join(lines)


def build_model_payload(rows: list[dict[str, Any]], model_name: str) -> dict[str, Any]:
    model_rows = [row for row in rows if row["model"] == model_name]
    run_ids = sorted({row["run"] for row in model_rows})
    binary_tests: list[dict[str, Any]] = []
    for metric in BINARY_METRICS:
        metric_results = [
            mcnemar_result(rows, model_name, metric, order_name)
            for order_name in COMPARED_ORDERS
        ]
        adjusted = holm_adjust(metric_results, "p_value")
        for result, p_holm in zip(metric_results, adjusted):
            result["p_value_holm"] = p_holm
        binary_tests.extend(metric_results)

    for metric in CONDITIONAL_BINARY_METRICS:
        metric_results = [
            mcnemar_result(
                rows,
                model_name,
                metric,
                order_name,
                require_both_executable=True,
            )
            for order_name in COMPARED_ORDERS
        ]
        adjusted = holm_adjust(metric_results, "p_value")
        for result, p_holm in zip(metric_results, adjusted):
            result["p_value_holm"] = p_holm
        binary_tests.extend(metric_results)

    numeric_tests: list[dict[str, Any]] = []
    for metric in NUMERIC_METRICS:
        metric_results = [
            numeric_result(rows, model_name, metric, order_name)
            for order_name in COMPARED_ORDERS
        ]
        adjusted_t = holm_adjust(metric_results, "p_value_t_test")
        adjusted_perm = holm_adjust(metric_results, "p_value_sign_flip_permutation")
        for result, p_t_holm, p_perm_holm in zip(metric_results, adjusted_t, adjusted_perm):
            result["p_value_t_test_holm"] = p_t_holm
            result["p_value_sign_flip_permutation_holm"] = p_perm_holm
        numeric_tests.extend(metric_results)

    return {
        "model": model_name,
        "generated_from": str(DATA_ROOT),
        "row_count": len(model_rows),
        "problem_count": len({row["problem"] for row in model_rows}),
        "run_ids": run_ids,
        "orders": VARIANT_NAMES,
        "baseline_order": BASELINE_ORDER,
        "compared_orders": COMPARED_ORDERS,
        "method_summary": {
            "binary": "Exact McNemar test on paired binary outcomes.",
            "conditional_binary": "Exact McNemar test after filtering to pairs where both orders are executable.",
            "numeric": "Paired t-test and paired sign-flip permutation test.",
            "multiple_comparisons": "Holm adjustment across the three order comparisons within each model/metric/test family.",
        },
        "metric_definitions": {
            **BINARY_METRICS,
            **CONDITIONAL_BINARY_METRICS,
            **NUMERIC_METRICS,
        },
        "binary_tests": binary_tests,
        "numeric_tests": numeric_tests,
    }


def main() -> None:
    rows = load_rows()
    (OUTPUT_DIR / "input_rows.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    index_lines = [
        "# Statistical Testing",
        "",
        "This folder contains reproducible order-effect tests for the saved local `llm_result.json` files. No model/API calls are made.",
        "",
        "Pairing is done within each model by `(problem, run)`: each compared order is matched with `canonical` for the same problem and run.",
        "",
        "Binary metrics use exact McNemar tests. Numeric metrics use paired t-tests and sign-flip permutation tests.",
        "",
        "Files:",
    ]

    for model_name in MODEL_NAMES:
        payload = build_model_payload(rows, model_name)
        slug = model_output_dir_name(model_name)
        json_path = OUTPUT_DIR / f"{slug}_stats.json"
        md_path = OUTPUT_DIR / f"{slug}_stats.md"
        csv_path = OUTPUT_DIR / f"{slug}_tests.csv"
        json_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        md_path.write_text(markdown_report(model_name, payload), encoding="utf-8")
        write_csv(csv_path, payload["binary_tests"] + payload["numeric_tests"])
        index_lines.append(f"- `{json_path.name}` / `{md_path.name}` / `{csv_path.name}`")

    (OUTPUT_DIR / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"Wrote statistical test outputs to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
