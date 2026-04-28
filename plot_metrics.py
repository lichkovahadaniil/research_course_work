import os
import shutil
import json
import math
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp")

import matplotlib
import pandas as pd
from matplotlib.patches import Patch
from matplotlib.ticker import PercentFormatter

from experiment_config import (
    MODEL_NAMES,
    PROBLEM_TYPE_BY_ID,
    PROBLEM_TYPE_LABELS,
    PROBLEM_TYPE_ORDER,
    ProblemRef,
)
from manual_model_run import model_output_dir_name
from shuffler import VARIANT_NAMES
from token_usage import build_token_usage_from_payload


matplotlib.use("Agg")
import matplotlib.pyplot as plt


RECORD_COLUMNS = [
    "domain",
    "problem",
    "task",
    "problem_type",
    "variant",
    "run",
    "model",
    "plan_length",
    "executability",
    "reachability",
    "conditional_reachability",
    "optimality_ratio",
    "first_failure_step",
    "non_executable_failure",
    "prompt_tokens",
    "completion_tokens",
    "total_tokens",
    "reasoning_completion_tokens",
    "raw_completion_tokens",
    "completion_token_breakdown_source",
]
METRICS = [
    {
        "slug": "plan_length",
        "title": "Plan Length",
        "subset": "reachable",
        "rate": False,
    },
    {
        "slug": "executability",
        "title": "Executability",
        "subset": "all",
        "rate": True,
    },
    {
        "slug": "reachability",
        "title": "Reachability",
        "subset": "all",
        "rate": True,
    },
    {
        "slug": "conditional_reachability",
        "title": "Conditional Reachability",
        "subset": "all",
        "rate": True,
    },
    {
        "slug": "optimality_ratio",
        "title": "Optimality Ratio",
        "subset": "reachable",
        "rate": False,
    },
    {
        "slug": "first_failure_step",
        "title": "First Failure Step",
        "subset": "failure_step",
        "rate": False,
    },
    {
        "slug": "non_executable_failure",
        "title": "Non-Executable Failure",
        "subset": "all",
        "rate": True,
    },
]


plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update(
    {
        "figure.figsize": (12, 6),
        "axes.titlesize": 14,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
    }
)


def _load_result(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _build_record(
    *,
    domain_name: str,
    task_name: str,
    problem_id: str,
    variant_name: str,
    run_id: int | None,
    model_name: str,
    payload: dict,
) -> dict:
    metrics = payload.get("metrics") or {}
    strict = metrics.get("strict") or {}
    legacy = metrics.get("legacy") or {}
    token_usage = build_token_usage_from_payload(payload)

    executability = bool(strict.get("executability"))
    reachability = bool(strict.get("reachability"))

    return {
        "domain": domain_name,
        "problem": problem_id,
        "task": task_name,
        "problem_type": PROBLEM_TYPE_BY_ID.get(problem_id, "unknown"),
        "variant": variant_name,
        "run": run_id,
        "model": model_name,
        "plan_length": strict.get("plan_length") if reachability else None,
        "executability": float(executability),
        "reachability": float(reachability),
        "conditional_reachability": float(executability and reachability),
        "optimality_ratio": legacy.get("optimality_ratio") if reachability else None,
        "first_failure_step": strict.get("first_failure_step"),
        "non_executable_failure": float(strict.get("non_executable_failure") is not None),
        "prompt_tokens": token_usage["prompt_tokens"],
        "completion_tokens": token_usage["completion_tokens"],
        "total_tokens": token_usage["total_tokens"],
        "reasoning_completion_tokens": token_usage["reasoning_completion_tokens"],
        "raw_completion_tokens": token_usage["raw_completion_tokens"],
        "completion_token_breakdown_source": token_usage["completion_token_breakdown_source"],
    }


def _variant_run_dirs(variant_dir: Path) -> list[Path]:
    if not variant_dir.exists():
        return []
    return sorted(
        [child for child in variant_dir.iterdir() if child.is_dir() and child.name.isdigit()],
        key=lambda child: int(child.name),
    )

MODERN_COLORS = ["#348ABD", "#E24A33", "#8EBA42"]

def _apply_modern_style(ax):
    """Делает график чистым и минималистичным."""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#DDDDDD')
    ax.spines['bottom'].set_color('#DDDDDD')
    
    # Легкая пунктирная сетка только по оси Y
    ax.grid(axis='y', linestyle='--', alpha=0.6, color='#CCCCCC')
    ax.grid(axis='x', visible=False)
    ax.set_axisbelow(True) # Сетка прячется за столбцами

def _add_value_labels(ax, is_rate: bool):
    """Добавляет цифры над каждым столбцом."""
    for p in ax.patches:
        height = p.get_height()
        if not math.isfinite(height) or abs(height) <= 0.001:
            continue
        if is_rate:
            text = f"{height:.0%}" # Формат 85%
        else:
            text = f"{int(height)}" if height.is_integer() else f"{height:.1f}"

        ax.annotate(text,
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom',
                    xytext=(0, 4), # Сдвиг на 4 пикселя вверх
                    textcoords='offset points',
                    fontsize=9,
                    color='#444444')
            
def build_records(domains: list[str], problem_refs: list[ProblemRef]) -> pd.DataFrame:
    records: list[dict] = []

    for domain_name in domains:
        for problem_ref in problem_refs:
            problem_dir = Path("materials") / domain_name / problem_ref.task / problem_ref.problem
            for variant_name in VARIANT_NAMES:
                variant_dir = problem_dir / variant_name
                run_dirs = _variant_run_dirs(variant_dir)
                for model_name in MODEL_NAMES:
                    model_dir_name = model_output_dir_name(model_name)
                    if run_dirs:
                        for run_dir in run_dirs:
                            result_path = run_dir / model_dir_name / "llm_result.json"
                            if not result_path.exists():
                                continue
                            records.append(
                                _build_record(
                                    domain_name=domain_name,
                                    task_name=problem_ref.task,
                                    problem_id=problem_ref.problem,
                                    variant_name=variant_name,
                                    run_id=int(run_dir.name),
                                    model_name=model_name,
                                    payload=_load_result(result_path),
                                )
                            )
                        continue

                    legacy_result_path = variant_dir / model_dir_name / "llm_result.json"
                    if not legacy_result_path.exists():
                        continue
                    records.append(
                        _build_record(
                            domain_name=domain_name,
                            task_name=problem_ref.task,
                            problem_id=problem_ref.problem,
                            variant_name=variant_name,
                            run_id=None,
                            model_name=model_name,
                            payload=_load_result(legacy_result_path),
                        )
                    )

    return pd.DataFrame(records, columns=RECORD_COLUMNS)


def summarize_records(records: pd.DataFrame, metric_slug: str) -> pd.DataFrame:
    if records.empty:
        return pd.DataFrame(columns=["variant", "model", metric_slug])
    return (
        records.groupby(["variant", "model"], as_index=False)[metric_slug]
        .mean()
        .sort_values(["variant", "model"])
        .reset_index(drop=True)
    )


def summarize_problem_type_records(records: pd.DataFrame, metric_slug: str) -> pd.DataFrame:
    if records.empty:
        return pd.DataFrame(columns=["problem_type", "variant", "model", metric_slug])
    return (
        records.groupby(["problem_type", "variant", "model"], as_index=False)[metric_slug]
        .mean()
        .sort_values(["problem_type", "variant", "model"])
        .reset_index(drop=True)
    )


def summarize_token_records(records: pd.DataFrame) -> pd.DataFrame:
    token_columns = [
        "completion_tokens",
        "reasoning_completion_tokens",
        "raw_completion_tokens",
    ]
    if records.empty:
        return pd.DataFrame(columns=["variant", "model", *token_columns])
    return (
        records.groupby(["variant", "model"], as_index=False)[token_columns]
        .mean()
        .sort_values(["variant", "model"])
        .reset_index(drop=True)
    )


def _metric_subset(records: pd.DataFrame, metric: dict) -> pd.DataFrame:
    slug = metric["slug"]
    subset = metric["subset"]

    if subset == "reachable":
        return records[records["reachability"] == 1.0].copy()
    if subset == "failure_step":
        return records[records[slug].notna()].copy()
    return records[records[slug].notna()].copy()


def _metric_title(metric: dict, coverage_ratio: float) -> str:
    if metric["subset"] == "reachable":
        return f"{metric['title']} (only reachable, {coverage_ratio:.0%})"
    if metric["subset"] == "failure_step":
        return f"{metric['title']} (available, {coverage_ratio:.0%})"
    return f"{metric['title']} ({coverage_ratio:.0%})"


def _token_breakdown_title(coverage_ratio: float) -> str:
    return f"Completion Token Breakdown ({coverage_ratio:.0%})"


def _plot_problem_variant_bar(frame: pd.DataFrame, metric: dict, output_path: Path, title: str) -> None:
    if frame.empty:
        return

    pivot = (
        summarize_records(frame, metric["slug"])
        .pivot(index="variant", columns="model", values=metric["slug"])
        .reindex(index=VARIANT_NAMES, columns=MODEL_NAMES)
    )

    ax = pivot.plot(
        kind="bar", 
        width=0.8,
        figsize=(10, 6),
        color=MODERN_COLORS,
        edgecolor="none" # Убираем черную обводку самих столбцов
    )
    
    ax.set_title(title, pad=20, fontsize=14, fontweight='bold', color='#333333')
    ax.set_ylabel(f"Average {metric['title']}", fontsize=11, color='#555555')
    ax.set_xlabel("Variant", fontsize=11, color='#555555')
    
    _apply_modern_style(ax)
    _add_value_labels(ax, is_rate=metric["rate"])
    ax.legend(title="Models", bbox_to_anchor=(1.02, 1), loc='upper left', frameon=False, title_fontsize='12')
    
    if metric["rate"]:
        ax.set_ylim(0, 1.15) # Увеличенный запас сверху для цифр
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
    else:
        ax.set_ylim(0, ax.get_ylim()[1] * 1.15)
    
    plt.xticks(rotation=0, color='#333333')
    plt.yticks(color='#333333')
    plt.tight_layout()
    
    plt.savefig(output_path, dpi=300, bbox_inches="tight") # dpi=300 для высокой четкости
    plt.close()


def _plot_problem_type_bar(frame: pd.DataFrame, metric: dict, output_path: Path, title: str) -> None:
    if frame.empty:
        return

    summary = summarize_problem_type_records(frame, metric["slug"])
    if summary.empty:
        return

    summary_lookup = {
        (row.problem_type, row.variant, row.model): getattr(row, metric["slug"])
        for row in summary.itertuples(index=False)
    }
    clusters: list[tuple[str, str]] = [
        (problem_type, variant_name)
        for problem_type in PROBLEM_TYPE_ORDER
        for variant_name in VARIANT_NAMES
    ]
    cluster_positions: list[float] = []
    type_centers: list[float] = []
    position = 0.0
    for problem_type in PROBLEM_TYPE_ORDER:
        start_position = position
        for variant_name in VARIANT_NAMES:
            cluster_positions.append(position)
            position += 1.0
        type_centers.append((start_position + position - 1.0) / 2)
        position += 0.75

    fig, ax = plt.subplots(figsize=(24, 7))
    width = 0.78 / max(len(MODEL_NAMES), 1)
    max_height = 0.0
    for model_index, model_name in enumerate(MODEL_NAMES):
        color = MODERN_COLORS[model_index % len(MODERN_COLORS)]
        offset = (model_index - (len(MODEL_NAMES) - 1) / 2) * width
        values = [
            summary_lookup.get((problem_type, variant_name, model_name), float("nan"))
            for problem_type, variant_name in clusters
        ]
        finite_values = [value for value in values if math.isfinite(value)]
        if finite_values:
            max_height = max(max_height, max(finite_values))
        ax.bar(
            [cluster_position + offset for cluster_position in cluster_positions],
            values,
            width=width * 0.92,
            color=color,
            edgecolor="none",
            label=model_name,
        )

    ax.set_title(title, pad=20, fontsize=14, fontweight="bold", color="#333333")
    ax.set_ylabel(f"Average {metric['title']}", fontsize=11, color="#555555")
    ax.set_xlabel("Problem type / order", fontsize=11, color="#555555")
    ax.set_xticks(cluster_positions)
    ax.set_xticklabels([variant_name for _, variant_name in clusters], rotation=45, ha="right")

    for boundary_index in range(1, len(PROBLEM_TYPE_ORDER)):
        boundary_position = boundary_index * len(VARIANT_NAMES) + (boundary_index - 1) * 0.75 - 0.125
        ax.axvline(boundary_position, color="#DDDDDD", linewidth=1.0)
    for center, problem_type in zip(type_centers, PROBLEM_TYPE_ORDER):
        ax.text(
            center,
            -0.22,
            PROBLEM_TYPE_LABELS.get(problem_type, problem_type),
            transform=ax.get_xaxis_transform(),
            ha="center",
            va="top",
            fontsize=9,
            color="#333333",
            fontweight="bold",
        )

    _apply_modern_style(ax)
    ax.legend(title="Models", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False, title_fontsize="12")

    if metric["rate"]:
        ax.set_ylim(0, 1.15)
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
    else:
        ax.set_ylim(0, max_height * 1.15 if max_height > 0 else 1.0)

    plt.yticks(color="#333333")
    fig.subplots_adjust(bottom=0.28, right=0.84)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _plot_single_problem_type_bar(
    frame: pd.DataFrame,
    metric: dict,
    output_path: Path,
    title: str,
) -> None:
    if frame.empty:
        return

    pivot = (
        summarize_records(frame, metric["slug"])
        .pivot(index="variant", columns="model", values=metric["slug"])
        .reindex(index=VARIANT_NAMES, columns=MODEL_NAMES)
    )
    ax = pivot.plot(
        kind="bar",
        width=0.8,
        figsize=(10, 5.5),
        color=MODERN_COLORS,
        edgecolor="none",
    )

    ax.set_title(title, pad=18, fontsize=13, fontweight="bold", color="#333333")
    ax.set_ylabel(f"Average {metric['title']}", fontsize=11, color="#555555")
    ax.set_xlabel("Order", fontsize=11, color="#555555")

    _apply_modern_style(ax)
    _add_value_labels(ax, is_rate=metric["rate"])

    if metric["rate"]:
        ax.set_ylim(0, 1.15)
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
    else:
        ax.set_ylim(0, ax.get_ylim()[1] * 1.15)

    ax.legend(title="Models", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False, title_fontsize="12")
    plt.xticks(rotation=0, color="#333333")
    plt.yticks(color="#333333")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def _token_breakdown_subset(records: pd.DataFrame) -> pd.DataFrame:
    return records[
        records["completion_tokens"].notna()
        & records["reasoning_completion_tokens"].notna()
        & records["raw_completion_tokens"].notna()
    ].copy()


def _add_token_share_label(ax, x: float, y: float, share: float, color: str) -> None:
    ax.text(
        x,
        y,
        f"{share:.0%}",
        ha="center",
        va="center",
        fontsize=8,
        color=color,
        fontweight="bold",
    )


def _plot_problem_token_breakdown(frame: pd.DataFrame, output_path: Path, title: str) -> None:
    if frame.empty:
        return

    summary = summarize_token_records(frame)
    if summary.empty:
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.8 / max(len(MODEL_NAMES), 1)
    variant_positions = list(range(len(VARIANT_NAMES)))
    max_height = 0.0

    model_handles = []
    for model_index, model_name in enumerate(MODEL_NAMES):
        color = MODERN_COLORS[model_index % len(MODERN_COLORS)]
        offset = (model_index - (len(MODEL_NAMES) - 1) / 2) * width
        x_positions = [position + offset for position in variant_positions]
        model_summary = (
            summary[summary["model"] == model_name]
            .set_index("variant")
            .reindex(VARIANT_NAMES)
            .fillna(0.0)
        )
        reasoning_values = model_summary["reasoning_completion_tokens"].tolist()
        raw_values = model_summary["raw_completion_tokens"].tolist()
        total_values = [
            reasoning_value + raw_value
            for reasoning_value, raw_value in zip(reasoning_values, raw_values)
        ]

        reasoning_bars = ax.bar(
            x_positions,
            reasoning_values,
            width=width * 0.92,
            color=color,
            alpha=0.9,
            edgecolor="none",
        )
        raw_bars = ax.bar(
            x_positions,
            raw_values,
            width=width * 0.92,
            bottom=reasoning_values,
            color=color,
            alpha=0.45,
            edgecolor="none",
        )

        for reasoning_bar, raw_bar, reasoning_value, raw_value, total_value in zip(
            reasoning_bars,
            raw_bars,
            reasoning_values,
            raw_values,
            total_values,
        ):
            if not math.isfinite(total_value) or total_value <= 0:
                continue
            if reasoning_value > 0:
                _add_token_share_label(
                    ax,
                    reasoning_bar.get_x() + reasoning_bar.get_width() / 2,
                    reasoning_value / 2,
                    reasoning_value / total_value,
                    "white",
                )
            if raw_value > 0:
                _add_token_share_label(
                    ax,
                    raw_bar.get_x() + raw_bar.get_width() / 2,
                    reasoning_value + raw_value / 2,
                    raw_value / total_value,
                    "#222222",
                )

        max_height = max(max_height, *(total_values or [0.0]))
        model_handles.append(Patch(facecolor=color, alpha=0.9, label=model_name))

    ax.set_title(title, pad=20, fontsize=14, fontweight="bold", color="#333333")
    ax.set_ylabel("Average completion tokens", fontsize=11, color="#555555")
    ax.set_xlabel("Variant", fontsize=11, color="#555555")
    ax.set_xticks(variant_positions)
    ax.set_xticklabels(VARIANT_NAMES)

    _apply_modern_style(ax)

    model_legend = ax.legend(
        handles=model_handles,
        title="Models",
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        frameon=False,
        title_fontsize="12",
    )
    ax.add_artist(model_legend)
    ax.legend(
        handles=[
            Patch(facecolor="#666666", alpha=0.9, label="Reasoning tokens"),
            Patch(facecolor="#666666", alpha=0.45, label="Raw answer tokens"),
        ],
        title="Token Type",
        bbox_to_anchor=(1.02, 0.7),
        loc="upper left",
        frameon=False,
        title_fontsize="12",
    )

    ax.set_ylim(0, max_height * 1.12 if max_height > 0 else 1.0)
    plt.xticks(rotation=0, color="#333333")
    plt.yticks(color="#333333")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def build_reports(domains: list[str], problem_refs: list[ProblemRef]) -> None:
    all_records = build_records(domains, problem_refs)

    for domain_name in domains:
        domain_records = all_records[all_records["domain"] == domain_name].copy()
        graph_dir = Path("materials") / domain_name / "graph"
        if graph_dir.exists():
            shutil.rmtree(graph_dir)
        graph_dir.mkdir(parents=True, exist_ok=True)

        for problem_ref in problem_refs:
            (graph_dir / problem_ref.task / problem_ref.problem).mkdir(parents=True, exist_ok=True)
        for problem_ref in problem_refs:
            problem_records = domain_records[
                (domain_records["task"] == problem_ref.task)
                & (domain_records["problem"] == problem_ref.problem)
            ].copy()
            problem_dir = graph_dir / problem_ref.task / problem_ref.problem
            if problem_records.empty:
                continue
            problem_label = problem_ref.label

            for metric in METRICS:
                metric_records = _metric_subset(problem_records, metric)
                coverage_ratio = len(metric_records) / len(problem_records)
                _plot_problem_variant_bar(
                    metric_records,
                    metric,
                    problem_dir / f"{metric['slug']}_barplot.png",
                    f"{_metric_title(metric, coverage_ratio)} by variant - {problem_label}",
                )

            token_records = _token_breakdown_subset(problem_records)
            token_coverage_ratio = len(token_records) / len(problem_records)
            _plot_problem_token_breakdown(
                token_records,
                problem_dir / "completion_token_breakdown_barplot.png",
                f"{_token_breakdown_title(token_coverage_ratio)} by variant - {problem_label}",
            )

        type_graph_dir = graph_dir / "by_problem_type"
        type_graph_dir.mkdir(parents=True, exist_ok=True)
        for problem_type in PROBLEM_TYPE_ORDER:
            (type_graph_dir / problem_type).mkdir(parents=True, exist_ok=True)
        if domain_records.empty:
            continue

        for metric in METRICS:
            metric_records = _metric_subset(domain_records, metric)
            if metric_records.empty:
                continue

            coverage_ratio = len(metric_records) / len(domain_records)
            _plot_problem_type_bar(
                metric_records,
                metric,
                type_graph_dir / f"{metric['slug']}_by_problem_type_and_order_barplot.png",
                f"{_metric_title(metric, coverage_ratio)} by problem type and order",
            )

            for problem_type in PROBLEM_TYPE_ORDER:
                type_records = metric_records[metric_records["problem_type"] == problem_type].copy()
                if type_records.empty:
                    continue
                type_all_records = domain_records[domain_records["problem_type"] == problem_type]
                type_coverage_ratio = len(type_records) / len(type_all_records) if len(type_all_records) else 0.0
                single_type_dir = type_graph_dir / problem_type
                single_type_dir.mkdir(parents=True, exist_ok=True)
                _plot_single_problem_type_bar(
                    type_records,
                    metric,
                    single_type_dir / f"{metric['slug']}_barplot.png",
                    f"{_metric_title(metric, type_coverage_ratio)} - {PROBLEM_TYPE_LABELS.get(problem_type, problem_type)}",
                )
