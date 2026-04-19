import os
import re
import signal
import subprocess
import tempfile
import time
from functools import lru_cache
from pathlib import Path
from typing import Any


VALIDATE_TIMEOUT_SEC = 120
PLAN_COST_PATTERNS = (
    r"Optimal cost:\s*([0-9]+(?:\.[0-9]+)?)",
    r"Plan cost:\s*([0-9]+(?:\.[0-9]+)?)",
    r"Final value:\s*([0-9]+(?:\.[0-9]+)?)",
    r"Value:\s*([0-9]+(?:\.[0-9]+)?)",
)
PLAN_LENGTH_PATTERN = re.compile(r"Plan size:\s*(\d+)")
FIRST_FAILURE_PATTERNS = (
    re.compile(r"unsatisfied precondition at time\s+(\d+)", re.IGNORECASE),
    re.compile(r"Checking next happening \(time\s+(\d+)\)\s*[\r\n]+Plan failed", re.IGNORECASE),
)
ACTION_LINE_PATTERN = re.compile(r"^\s*\(([^;].*)\)\s*$")


def _read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def extract_numeric_value(text: str, patterns: tuple[str, ...] = PLAN_COST_PATTERNS) -> float | None:
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1))
    return None


def read_plan_actions(plan_path: str | Path) -> list[str]:
    actions: list[str] = []
    for raw_line in _read_text(plan_path).splitlines():
        line = raw_line.strip()
        if ACTION_LINE_PATTERN.match(line):
            actions.append(" ".join(line.lower().split()))
    return actions


def get_plan_cost(plan_path: str | Path) -> int:
    return len(read_plan_actions(plan_path))


def _run_validator(flag: str, domain_path: str | Path, problem_path: str | Path, plan_path: str | Path) -> tuple[int | None, str, bool]:
    with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8") as output_handle:
        process = subprocess.Popen(
            ["validate", flag, str(domain_path), str(problem_path), str(plan_path)],
            stdout=output_handle,
            stderr=subprocess.STDOUT,
            text=True,
            start_new_session=True,
        )

        deadline = time.monotonic() + VALIDATE_TIMEOUT_SEC
        timed_out = False

        while True:
            return_code = process.poll()
            if return_code is not None:
                break

            if time.monotonic() >= deadline:
                timed_out = True
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.kill()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    pass
                break

            time.sleep(0.25)

        output_handle.flush()
        output_handle.seek(0)
        output = output_handle.read()

    if timed_out:
        output = f"{output}\nValidator timed out after {VALIDATE_TIMEOUT_SEC} seconds.\n"
        return None, output, True

    return process.returncode, output, False


def extract_plan_length(output: str, plan_path: str | Path | None = None) -> int | None:
    match = PLAN_LENGTH_PATTERN.search(output)
    if match:
        return int(match.group(1))
    if plan_path is not None:
        return len(read_plan_actions(plan_path))
    return None


def extract_first_failure_step(output: str) -> int | None:
    for pattern in FIRST_FAILURE_PATTERNS:
        match = pattern.search(output)
        if match:
            return int(match.group(1))
    return None


def parse_strict_validation_output(output: str, plan_path: str | Path | None = None, timed_out: bool = False) -> dict[str, Any]:
    parsable = not bool(
        re.search(r"Bad plan description|parse error|failed to parse", output, re.IGNORECASE)
    )
    executability = "Plan executed successfully - checking goal" in output or "Plan valid" in output
    reachability = "Plan valid" in output

    non_executable_failure = None
    if timed_out:
        non_executable_failure = "validator_timeout"
    elif not parsable:
        non_executable_failure = "parse_error"
    elif not executability:
        non_executable_failure = "state_execution_error"

    return {
        "parsable": parsable,
        "plan_length": extract_plan_length(output, plan_path=plan_path),
        "executability": executability,
        "reachability": reachability,
        "first_failure_step": extract_first_failure_step(output) if non_executable_failure == "state_execution_error" else None,
        "non_executable_failure": non_executable_failure,
        "strict_final_value": extract_numeric_value(output) if reachability else None,
        "validator_timed_out": timed_out,
        "validator_stdout_strict": output,
    }


def parse_legacy_validation_output(output: str) -> dict[str, Any]:
    return {
        "cost": extract_numeric_value(output),
        "goal_reached": "Plan valid" in output,
        "validator_stdout_legacy": output,
    }


def strict_validation(domain_path: str | Path, problem_path: str | Path, plan_path: str | Path) -> dict[str, Any]:
    _, output, timed_out = _run_validator("-v", domain_path, problem_path, plan_path)
    return parse_strict_validation_output(output, plan_path=plan_path, timed_out=timed_out)


def legacy_validation(domain_path: str | Path, problem_path: str | Path, plan_path: str | Path) -> dict[str, Any]:
    _, output, timed_out = _run_validator("-c", domain_path, problem_path, plan_path)
    parsed = parse_legacy_validation_output(output)
    parsed["validator_timed_out"] = timed_out
    return parsed


def _sequence_lcs_length(left: list[str], right: list[str]) -> int:
    if not left or not right:
        return 0

    # The plans are short enough that a simple DP keeps the metric easy to reason about.
    previous = [0] * (len(right) + 1)
    for left_item in left:
        current = [0]
        for index, right_item in enumerate(right, start=1):
            if left_item == right_item:
                current.append(previous[index - 1] + 1)
            else:
                current.append(max(current[-1], previous[index]))
        previous = current
    return previous[-1]


def _legacy_action_name_distance(llm_plan_path: str | Path, optimal_plan_path: str | Path) -> dict[str, Any]:
    llm_seq = [action.split()[0].lstrip("(") for action in read_plan_actions(llm_plan_path)]
    opt_seq = [action.split()[0].lstrip("(") for action in read_plan_actions(optimal_plan_path)]

    common = [action for action in opt_seq if action in llm_seq]

    def kendall_tau(order1: list[str], order2: list[str]) -> int:
        pos = {action: idx for idx, action in enumerate(order2)}
        inversions = 0
        for idx in range(len(order1)):
            for jdx in range(idx + 1, len(order1)):
                if pos.get(order1[idx], -1) > pos.get(order1[jdx], -1):
                    inversions += 1
        return inversions

    tau = kendall_tau([action for action in llm_seq if action in common], common) if len(common) >= 2 else 0
    insertions = len(llm_seq) - len(common)
    deletions = len(opt_seq) - len(common)
    total_distance = tau + insertions + deletions
    max_possible = len(opt_seq) * (len(opt_seq) - 1) // 2 + len(opt_seq)

    return {
        "kendall_tau_inversions": tau,
        "insertions": insertions,
        "deletions": deletions,
        "total_distance": total_distance,
        "normalized_distance": round(total_distance / max_possible, 4) if max_possible else 0.0,
    }


def action_sequence_distance(llm_plan_path: str | Path, optimal_plan_path: str | Path) -> dict[str, Any]:
    llm_seq = read_plan_actions(llm_plan_path)
    opt_seq = read_plan_actions(optimal_plan_path)

    lcs_length = _sequence_lcs_length(llm_seq, opt_seq)
    insertions = len(llm_seq) - lcs_length
    deletions = len(opt_seq) - lcs_length
    total_distance = insertions + deletions
    denominator = max(len(llm_seq) + len(opt_seq), 1)

    return {
        "matching_actions": lcs_length,
        "insertions": insertions,
        "deletions": deletions,
        "total_distance": total_distance,
        "normalized_distance": round(total_distance / denominator, 4),
        "llm_actions_count": len(llm_seq),
        "optimal_actions_count": len(opt_seq),
        "deprecated_action_name_distance": _legacy_action_name_distance(llm_plan_path, optimal_plan_path),
    }


@lru_cache(maxsize=None)
def load_reference_plan_stats(
    domain_path: str,
    problem_path: str,
    optimal_plan_path: str,
) -> dict[str, Any]:
    optimal_path = Path(optimal_plan_path)
    optimal_cost = extract_numeric_value(_read_text(optimal_path))

    if optimal_cost is None:
        optimal_cost = legacy_validation(domain_path, problem_path, optimal_path)["cost"]

    return {
        "optimal_cost": optimal_cost,
        "optimal_plan_length": len(read_plan_actions(optimal_path)),
    }


def build_metrics(
    domain_path: str | Path,
    problem_path: str | Path,
    plan_path: str | Path,
    optimal_plan_path: str | Path | None = None,
) -> dict[str, Any]:
    strict = strict_validation(domain_path, problem_path, plan_path)
    if strict["reachability"]:
        legacy_raw = legacy_validation(domain_path, problem_path, plan_path)
    else:
        legacy_raw = {
            "cost": None,
            "goal_reached": False,
            "validator_stdout_legacy": None,
            "validator_timed_out": False,
            "skipped_because_strict_not_reached": True,
        }

    optimal_cost = None
    optimal_plan_length = None
    order_metric = None

    if optimal_plan_path and Path(optimal_plan_path).exists():
        reference = load_reference_plan_stats(
            str(Path(domain_path)),
            str(Path(problem_path)),
            str(Path(optimal_plan_path)),
        )
        optimal_cost = reference["optimal_cost"]
        optimal_plan_length = reference["optimal_plan_length"]
        order_metric = action_sequence_distance(plan_path, optimal_plan_path)

    legacy_cost = legacy_raw["cost"]
    reachability = strict["reachability"]

    gap = None
    optimality_ratio = None
    if reachability and legacy_cost is not None and optimal_cost not in (None, 0):
        gap = (legacy_cost - optimal_cost) / optimal_cost
        optimality_ratio = legacy_cost / optimal_cost

    bug_optimal = bool(
        reachability
        and legacy_cost is not None
        and optimal_cost is not None
        and legacy_cost < optimal_cost - 1e-6
    )

    legacy = {
        "cost": legacy_cost if reachability else None,
        "gap": gap,
        "bug_optimal": bug_optimal,
        "optimality_ratio": optimality_ratio,
        "validator_stdout_legacy": legacy_raw["validator_stdout_legacy"],
        "validator_timed_out": legacy_raw.get("validator_timed_out", False),
        "skipped_because_strict_not_reached": legacy_raw.get("skipped_because_strict_not_reached", False),
    }

    return {
        "strict": strict,
        "legacy": legacy,
        "order": order_metric,
        "reference": {
            "optimal_cost": optimal_cost,
            "optimal_plan_length": optimal_plan_length,
        },
    }
