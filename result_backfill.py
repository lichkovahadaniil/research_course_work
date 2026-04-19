import json
from pathlib import Path
from statistics import mean
from typing import Any


NUMERIC_RUNTIME_FIELDS = {
    "duration_sec": 2,
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0,
}
BOOL_RUNTIME_FIELDS = ("reasoning_enabled",)


def load_json_dict(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None

    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except json.JSONDecodeError:
        return None

    return payload if isinstance(payload, dict) else None


def result_payload_is_complete(payload: dict[str, Any] | None) -> bool:
    if not payload:
        return False

    metrics = payload.get("metrics")
    if not isinstance(metrics, dict):
        return False

    required_sections = {"strict", "legacy", "order"}
    return required_sections.issubset(metrics)


def _iter_peer_result_payloads(variant_dir: Path, model_dir_name: str) -> list[dict[str, Any]]:
    problem_dir = variant_dir.parent
    payloads: list[dict[str, Any]] = []

    for peer_variant_dir in sorted(child for child in problem_dir.iterdir() if child.is_dir()):
        if peer_variant_dir == variant_dir or not (peer_variant_dir / "domain.pddl").exists():
            continue

        peer_result_path = peer_variant_dir / model_dir_name / "llm_result.json"
        payload = load_json_dict(peer_result_path)
        if payload is not None:
            payloads.append(payload)

    return payloads


def _average_numeric_field(payloads: list[dict[str, Any]], field_name: str, precision: int) -> float | int | None:
    values = [
        payload.get(field_name)
        for payload in payloads
        if isinstance(payload.get(field_name), (int, float))
    ]
    if not values:
        return None

    averaged = mean(values)
    if precision == 0:
        return int(round(averaged))
    return round(averaged, precision)


def _majority_bool_field(payloads: list[dict[str, Any]], field_name: str) -> bool | None:
    values = [payload.get(field_name) for payload in payloads if isinstance(payload.get(field_name), bool)]
    if not values:
        return None

    true_count = sum(1 for value in values if value)
    return true_count >= (len(values) / 2)


def fill_missing_runtime_fields(
    payload: dict[str, Any],
    *,
    variant_dir: Path,
    model_dir_name: str,
) -> dict[str, Any]:
    existing = dict(payload)
    peer_payloads = _iter_peer_result_payloads(variant_dir, model_dir_name)
    if not peer_payloads:
        return existing

    imputed_fields: dict[str, Any] = {}

    for field_name, precision in NUMERIC_RUNTIME_FIELDS.items():
        if existing.get(field_name) is not None:
            continue
        averaged = _average_numeric_field(peer_payloads, field_name, precision)
        if averaged is not None:
            existing[field_name] = averaged
            imputed_fields[field_name] = averaged

    for field_name in BOOL_RUNTIME_FIELDS:
        if existing.get(field_name) is not None:
            continue
        majority = _majority_bool_field(peer_payloads, field_name)
        if majority is not None:
            existing[field_name] = majority
            imputed_fields[field_name] = majority

    if imputed_fields:
        metadata = dict(existing.get("runtime_backfill") or {})
        metadata.update({
            "strategy": "peer_variant_mean_within_domain_problem_model",
            "peer_count": len(peer_payloads),
            "imputed_fields": imputed_fields,
        })
        existing["runtime_backfill"] = metadata

    return existing
