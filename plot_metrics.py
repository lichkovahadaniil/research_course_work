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
    "execution_progress",
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
        "subset": "all",
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
        "subset": "executable",
        "rate": True,
        "ylabel": "Goal reached among executable plans",
    },
    {
        "slug": "optimality_ratio",
        "title": "Optimality Ratio",
        "subset": "reachable",
        "rate": False,
    },
    {
        "slug": "execution_progress",
        "title": "Execution Progress",
        "subset": "all",
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
        "plan_length": strict.get("plan_length"),
        "executability": float(executability),
        "reachability": float(reachability),
        "conditional_reachability": float(reachability) if executability else None,
        "optimality_ratio": legacy.get("optimality_ratio") if reachability else None,
        "execution_progress": strict.get("execution_progress"),
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
CONFIDENCE_LEVEL_LABEL = "95%"
NORMAL_95_Z = 1.959963984540054
DESIGN_GRAPH_DIR_NAME = "design"
DESIGN_BACKGROUND = "#ffffff"
DESIGN_PANEL = "#FBF7EF"
DESIGN_INK = "#241C15"
DESIGN_MUTED = "#73675C"
DESIGN_GRID = "#D8CEC0"
DESIGN_COLORS = ["#C65F3D", "#38695B", "#8B6F47"]
DESIGN_VARIANT_LABELS = {
    "canonical": "канонический",
    "disp_1": "с разбросом\n1 уровня",
    "disp_2": "с разбросом\n2 уровня",
    "disp_3": "с разбросом\n3 уровня",
    "plan_front": "последовательный",
    "plan_scatter": "рассеянный",
}
DESIGN_MODEL_LABELS = {
    "deepseek/deepseek-v4-flash": "deepseek",
}
DESIGN_METRIC_LABELS = {
    "plan_length": {
        "title": "Длина плана",
        "ylabel": "Средняя длина плана",
    },
    "executability": {
        "title": "Исполнимость",
        "ylabel": "Доля исполнимых планов",
    },
    "reachability": {
        "title": "Достижение цели",
        "ylabel": "Доля планов, достигших цель",
    },
    "conditional_reachability": {
        "title": "Достижение цели среди исполнимых",
        "ylabel": "Доля достигших цель среди исполнимых планов",
    },
    "optimality_ratio": {
        "title": "Коэффициент оптимальности",
        "ylabel": "Отношение к оптимальной длине",
    },
    "execution_progress": {
        "title": "Прогресс исполнения",
        "ylabel": "Средняя доля выполненного плана",
    },
    "first_failure_step": {
        "title": "Первый шаг ошибки",
        "ylabel": "Средний шаг первой ошибки",
    },
    "non_executable_failure": {
        "title": "Неисполняемые планы",
        "ylabel": "Доля неисполняемых планов",
    },
}
CONFIDENCE_INTERVAL_COLUMNS = [
    "metric",
    "metric_title",
    "variant",
    "model",
    "mean",
    "ci95_low",
    "ci95_high",
    "n",
    "ci_method",
    "coverage_ratio",
]


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


def _format_metric_value(value: float, is_rate: bool) -> str:
    if not math.isfinite(value):
        return ""
    if is_rate:
        return f"{value:.0%}"
    if abs(value) >= 1000:
        return f"{value:,.0f}"
    if float(value).is_integer():
        return f"{int(value)}"
    if abs(value) >= 10:
        return f"{value:.1f}"
    return f"{value:.2f}"


def _t_critical_95(df: int) -> float:
    if df <= 0:
        return 0.0
    table = {
        1: 12.706,
        2: 4.303,
        3: 3.182,
        4: 2.776,
        5: 2.571,
        6: 2.447,
        7: 2.365,
        8: 2.306,
        9: 2.262,
        10: 2.228,
        11: 2.201,
        12: 2.179,
        13: 2.160,
        14: 2.145,
        15: 2.131,
        16: 2.120,
        17: 2.110,
        18: 2.101,
        19: 2.093,
        20: 2.086,
        21: 2.080,
        22: 2.074,
        23: 2.069,
        24: 2.064,
        25: 2.060,
        26: 2.056,
        27: 2.052,
        28: 2.048,
        29: 2.045,
        30: 2.042,
    }
    if df <= 30:
        return table[df]
    if df <= 40:
        return table[30]
    if df <= 60:
        return 2.021
    if df <= 120:
        return 2.000
    return 1.960


def _numeric_values(series: pd.Series) -> list[float]:
    values: list[float] = []
    for value in series.dropna().tolist():
        numeric_value = float(value)
        if math.isfinite(numeric_value):
            values.append(numeric_value)
    return values


def _mean_t_confidence_interval(values: list[float]) -> tuple[float, float, float, str]:
    mean = sum(values) / len(values)
    if len(values) == 1:
        return mean, mean, mean, "single_observation"

    variance = sum((value - mean) ** 2 for value in values) / (len(values) - 1)
    standard_error = math.sqrt(variance) / math.sqrt(len(values))
    margin = _t_critical_95(len(values) - 1) * standard_error
    return mean, mean - margin, mean + margin, "t_mean_95"


def _wilson_confidence_interval(values: list[float]) -> tuple[float, float, float, str]:
    mean = sum(values) / len(values)
    proportion = min(max(mean, 0.0), 1.0)
    sample_size = len(values)
    z_squared = NORMAL_95_Z ** 2
    denominator = 1 + z_squared / sample_size
    center = (proportion + z_squared / (2 * sample_size)) / denominator
    margin = (
        NORMAL_95_Z
        * math.sqrt(
            proportion * (1 - proportion) / sample_size
            + z_squared / (4 * sample_size * sample_size)
        )
        / denominator
    )
    return mean, max(0.0, center - margin), min(1.0, center + margin), "wilson_score_95"


def _confidence_interval(values: list[float], *, is_rate: bool) -> tuple[float, float, float, int, str]:
    if is_rate:
        mean, low, high, method = _wilson_confidence_interval(values)
    else:
        mean, low, high, method = _mean_t_confidence_interval(values)
    return mean, low, high, len(values), method
            
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


def summarize_confidence_intervals(
    records: pd.DataFrame,
    metric: dict,
    coverage_ratio: float = 1.0,
) -> pd.DataFrame:
    rows: list[dict] = []
    if records.empty:
        return pd.DataFrame(rows, columns=CONFIDENCE_INTERVAL_COLUMNS)

    metric_slug = metric["slug"]
    for (variant_name, model_name), group in records.groupby(["variant", "model"], sort=False):
        values = _numeric_values(group[metric_slug])
        if not values:
            continue

        mean, ci_low, ci_high, sample_size, ci_method = _confidence_interval(
            values,
            is_rate=metric["rate"],
        )
        rows.append(
            {
                "metric": metric_slug,
                "metric_title": metric["title"],
                "variant": variant_name,
                "model": model_name,
                "mean": mean,
                "ci95_low": ci_low,
                "ci95_high": ci_high,
                "n": sample_size,
                "ci_method": ci_method,
                "coverage_ratio": coverage_ratio,
            }
        )

    if not rows:
        return pd.DataFrame(rows, columns=CONFIDENCE_INTERVAL_COLUMNS)
    return (
        pd.DataFrame(rows, columns=CONFIDENCE_INTERVAL_COLUMNS)
        .sort_values(["metric", "variant", "model"])
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
    if subset == "executable":
        return records[
            (records["executability"] == 1.0)
            & records[slug].notna()
        ].copy()
    if subset == "failure_step":
        return records[records[slug].notna()].copy()
    return records[records[slug].notna()].copy()


def _metric_title(metric: dict, coverage_ratio: float) -> str:
    if metric["subset"] == "reachable":
        return f"{metric['title']} (only reachable, {coverage_ratio:.0%})"
    if metric["subset"] == "executable":
        return f"{metric['title']} (only executable plans, {coverage_ratio:.0%})"
    if metric["subset"] == "failure_step":
        return f"{metric['title']} (available, {coverage_ratio:.0%})"
    return f"{metric['title']} ({coverage_ratio:.0%})"


def _metric_ylabel(metric: dict) -> str:
    return metric.get("ylabel", f"Average {metric['title']}")


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
    ax.set_ylabel(_metric_ylabel(metric), fontsize=11, color='#555555')
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


def _ordered_values(values: pd.Series, preferred_order: list[str]) -> list[str]:
    present = list(dict.fromkeys(values.dropna().tolist()))
    ordered = [value for value in preferred_order if value in present]
    ordered.extend(sorted(value for value in present if value not in preferred_order))
    return ordered


def _apply_interval_style(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#DDDDDD")
    ax.grid(axis="x", linestyle="--", alpha=0.55, color="#CCCCCC")
    ax.grid(axis="y", visible=False)
    ax.tick_params(axis="y", length=0)
    ax.set_axisbelow(True)


def _set_interval_xlim(ax, summary: pd.DataFrame, metric: dict) -> None:
    if metric["rate"]:
        ax.set_xlim(0, 1.0)
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        return

    low = summary["ci95_low"].min()
    high = summary["ci95_high"].max()
    if not math.isfinite(low) or not math.isfinite(high):
        ax.set_xlim(0, 1)
        return

    minimum = min(0.0, low)
    maximum = high
    span = maximum - minimum
    if span <= 0:
        span = abs(maximum) if maximum else 1.0
    ax.set_xlim(minimum - span * 0.04, maximum + span * 0.16)


def _plot_confidence_intervals(frame: pd.DataFrame, metric: dict, output_path: Path, title: str) -> None:
    if frame.empty:
        return

    summary = summarize_confidence_intervals(frame, metric)
    if summary.empty:
        return

    variants = _ordered_values(summary["variant"], VARIANT_NAMES)
    models = _ordered_values(summary["model"], MODEL_NAMES)
    if not variants or not models:
        return

    fig_height = max(4.8, 1.0 + len(variants) * 0.78)
    fig, ax = plt.subplots(figsize=(11.5, fig_height))
    variant_positions = {variant_name: index for index, variant_name in enumerate(variants)}
    model_offset_step = 0.22 if len(models) > 1 else 0.0

    for position in range(len(variants)):
        if position % 2 == 0:
            ax.axhspan(position - 0.5, position + 0.5, color="#F7F8FA", zorder=0)

    for model_index, model_name in enumerate(models):
        color = MODERN_COLORS[model_index % len(MODERN_COLORS)]
        offset = (model_index - (len(models) - 1) / 2) * model_offset_step
        model_summary = summary[summary["model"] == model_name]
        x_values: list[float] = []
        y_values: list[float] = []
        xerr_low: list[float] = []
        xerr_high: list[float] = []

        for row in model_summary.itertuples(index=False):
            if row.variant not in variant_positions:
                continue
            mean = float(row.mean)
            ci_low = float(row.ci95_low)
            ci_high = float(row.ci95_high)
            if not all(math.isfinite(value) for value in [mean, ci_low, ci_high]):
                continue

            y = variant_positions[row.variant] + offset
            x_values.append(mean)
            y_values.append(y)
            xerr_low.append(max(0.0, mean - ci_low))
            xerr_high.append(max(0.0, ci_high - mean))
            ax.annotate(
                f"{_format_metric_value(mean, metric['rate'])}  n={row.n}",
                (ci_high, y),
                xytext=(7, 0),
                textcoords="offset points",
                ha="left",
                va="center",
                fontsize=8.5,
                color="#333333",
                clip_on=False,
            )

        if not x_values:
            continue
        ax.errorbar(
            x_values,
            y_values,
            xerr=[xerr_low, xerr_high],
            fmt="o",
            markersize=7.5,
            linewidth=0,
            elinewidth=3.0,
            capsize=5,
            capthick=2.3,
            color=color,
            ecolor=color,
            label=model_name,
            alpha=0.95,
            zorder=3,
        )

    ax.set_title(title, pad=18, fontsize=14, fontweight="bold", color="#333333")
    ax.set_xlabel(_metric_ylabel(metric), fontsize=11, color="#555555")
    ax.set_ylabel("Variant", fontsize=11, color="#555555")
    ax.set_yticks(list(variant_positions.values()))
    ax.set_yticklabels(variants, color="#333333")
    ax.invert_yaxis()
    _set_interval_xlim(ax, summary, metric)
    _apply_interval_style(ax)

    ax.legend(
        title="Models",
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        frameon=False,
        title_fontsize="12",
    )
    ax.text(
        0,
        -0.14,
        f"Dot = mean; whisker = {CONFIDENCE_LEVEL_LABEL} confidence interval.",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        color="#666666",
    )
    fig.subplots_adjust(right=0.78, bottom=0.18)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _design_variant_label(variant_name: str) -> str:
    return DESIGN_VARIANT_LABELS.get(variant_name, variant_name)


def _design_model_label(model_name: str) -> str:
    return DESIGN_MODEL_LABELS.get(model_name, model_name)


def _design_metric_title(metric: dict) -> str:
    return DESIGN_METRIC_LABELS.get(metric["slug"], {}).get("title", metric["title"])


def _design_metric_ylabel(metric: dict) -> str:
    return DESIGN_METRIC_LABELS.get(metric["slug"], {}).get("ylabel", _metric_ylabel(metric))


def _design_subset_note(metric: dict, coverage_ratio: float) -> str:
    if metric["subset"] == "reachable":
        return f"Только планы, достигшие цель; покрытие выборки {coverage_ratio:.0%}"
    if metric["subset"] == "executable":
        return f"Только исполнимые планы; покрытие выборки {coverage_ratio:.0%}"
    if metric["subset"] == "failure_step":
        return f"Только запуски с зафиксированной ошибкой; покрытие выборки {coverage_ratio:.0%}"
    return "Все запуски"


def _setup_design_figure(figsize: tuple[float, float] = (13.33, 7.5)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(DESIGN_BACKGROUND)
    ax.set_facecolor(DESIGN_PANEL)
    return fig, ax


def _apply_design_axis_style(ax, *, grid_axis: str) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(DESIGN_GRID)
    ax.spines["bottom"].set_color(DESIGN_GRID)
    ax.tick_params(colors=DESIGN_INK, labelsize=11)
    ax.grid(axis=grid_axis, color=DESIGN_GRID, linewidth=1.1, alpha=0.7)
    ax.grid(axis="x" if grid_axis == "y" else "y", visible=False)
    ax.set_axisbelow(True)


def _add_design_header(fig, title: str, subtitle: str) -> None:
    fig.text(
        0.06,
        0.94,
        title,
        ha="left",
        va="top",
        fontsize=23,
        fontweight="bold",
        color=DESIGN_INK,
    )
    fig.text(
        0.06,
        0.895,
        subtitle,
        ha="left",
        va="top",
        fontsize=12.5,
        color=DESIGN_MUTED,
    )


def _add_design_footer(fig, text: str) -> None:
    fig.text(
        0.06,
        0.055,
        text,
        ha="left",
        va="bottom",
        fontsize=10.5,
        color=DESIGN_MUTED,
    )


def _design_output_path(design_dir: Path, output_name: str) -> Path:
    design_dir.mkdir(parents=True, exist_ok=True)
    return design_dir / output_name


def _plot_design_order_bar(
    frame: pd.DataFrame,
    metric: dict,
    output_path: Path,
    coverage_ratio: float,
) -> None:
    if frame.empty:
        return

    pivot = (
        summarize_records(frame, metric["slug"])
        .pivot(index="variant", columns="model", values=metric["slug"])
        .reindex(index=VARIANT_NAMES, columns=MODEL_NAMES)
    )
    if pivot.empty:
        return

    fig, ax = _setup_design_figure()
    _add_design_header(
        fig,
        f"{_design_metric_title(metric)} по порядку действий",
        f"Столбец — среднее значение. {_design_subset_note(metric, coverage_ratio)}.",
    )

    variant_positions = list(range(len(VARIANT_NAMES)))
    width = 0.74 / max(len(MODEL_NAMES), 1)
    max_height = 0.0

    for model_index, model_name in enumerate(MODEL_NAMES):
        color = DESIGN_COLORS[model_index % len(DESIGN_COLORS)]
        offset = (model_index - (len(MODEL_NAMES) - 1) / 2) * width
        values = [
            float(value) if pd.notna(value) else math.nan
            for value in pivot.get(model_name, pd.Series(index=VARIANT_NAMES, dtype=float)).tolist()
        ]
        x_positions = [position + offset for position in variant_positions]
        bars = ax.bar(
            x_positions,
            values,
            width=width * 0.88,
            color=color,
            edgecolor="none",
            label=_design_model_label(model_name),
            alpha=0.96,
        )
        for bar, value in zip(bars, values):
            if not math.isfinite(value):
                continue
            max_height = max(max_height, value)
            ax.annotate(
                _format_metric_value(value, metric["rate"]),
                (bar.get_x() + bar.get_width() / 2, value),
                ha="center",
                va="bottom",
                xytext=(0, 7),
                textcoords="offset points",
                fontsize=10,
                color=DESIGN_INK,
            )

    ax.set_ylabel(_design_metric_ylabel(metric), fontsize=12.5, color=DESIGN_INK, labelpad=12)
    ax.set_xlabel("")
    ax.set_xticks(variant_positions)
    ax.set_xticklabels([_design_variant_label(variant) for variant in VARIANT_NAMES])
    if metric["rate"]:
        ax.set_ylim(0, 1.12)
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
    else:
        ax.set_ylim(0, max_height * 1.18 if max_height > 0 else 1.0)

    _apply_design_axis_style(ax, grid_axis="y")
    ax.legend(
        title="Модель",
        loc="upper right",
        bbox_to_anchor=(1.0, 1.18),
        frameon=False,
        ncol=len(MODEL_NAMES),
        fontsize=11,
        title_fontsize=11,
        labelcolor=DESIGN_INK,
    )
    _add_design_footer(fig, "Сводка по всем задачам и запускам.")
    fig.subplots_adjust(left=0.10, right=0.96, top=0.78, bottom=0.20)
    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def _set_design_interval_xlim(ax, summary: pd.DataFrame, metric: dict) -> None:
    if metric["rate"]:
        ax.set_xlim(0, 1.0)
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        return

    low = summary["ci95_low"].min()
    high = summary["ci95_high"].max()
    if not math.isfinite(low) or not math.isfinite(high):
        ax.set_xlim(0, 1)
        return
    minimum = min(0.0, low)
    maximum = high
    span = maximum - minimum
    if span <= 0:
        span = abs(maximum) if maximum else 1.0
    ax.set_xlim(minimum - span * 0.04, maximum + span * 0.20)


def _plot_design_confidence_intervals(
    frame: pd.DataFrame,
    metric: dict,
    output_path: Path,
    coverage_ratio: float,
) -> None:
    if frame.empty:
        return

    summary = summarize_confidence_intervals(frame, metric, coverage_ratio)
    if summary.empty:
        return

    variants = _ordered_values(summary["variant"], VARIANT_NAMES)
    models = _ordered_values(summary["model"], MODEL_NAMES)
    if not variants or not models:
        return

    fig, ax = _setup_design_figure()
    _add_design_header(
        fig,
        f"{_design_metric_title(metric)}: 95% доверительный интервал",
        f"Точка — среднее значение, отрезок — 95% ДИ. {_design_subset_note(metric, coverage_ratio)}.",
    )

    variant_positions = {variant_name: index for index, variant_name in enumerate(variants)}
    model_offset_step = 0.24 if len(models) > 1 else 0.0

    for position in range(len(variants)):
        if position % 2 == 0:
            ax.axhspan(position - 0.5, position + 0.5, color="#F0E8DC", zorder=0)

    for model_index, model_name in enumerate(models):
        color = DESIGN_COLORS[model_index % len(DESIGN_COLORS)]
        offset = (model_index - (len(models) - 1) / 2) * model_offset_step
        model_summary = summary[summary["model"] == model_name]
        x_values: list[float] = []
        y_values: list[float] = []
        xerr_low: list[float] = []
        xerr_high: list[float] = []

        for row in model_summary.itertuples(index=False):
            if row.variant not in variant_positions:
                continue
            mean = float(row.mean)
            ci_low = float(row.ci95_low)
            ci_high = float(row.ci95_high)
            if not all(math.isfinite(value) for value in [mean, ci_low, ci_high]):
                continue
            y = variant_positions[row.variant] + offset
            x_values.append(mean)
            y_values.append(y)
            xerr_low.append(max(0.0, mean - ci_low))
            xerr_high.append(max(0.0, ci_high - mean))
            ax.annotate(
                _format_metric_value(mean, metric["rate"]),
                (ci_high, y),
                xytext=(9, 0),
                textcoords="offset points",
                ha="left",
                va="center",
                fontsize=10,
                color=DESIGN_INK,
                clip_on=False,
            )

        if not x_values:
            continue
        ax.errorbar(
            x_values,
            y_values,
            xerr=[xerr_low, xerr_high],
            fmt="o",
            markersize=8.2,
            linewidth=0,
            elinewidth=3.2,
            capsize=5,
            capthick=2.2,
            color=color,
            ecolor=color,
            label=_design_model_label(model_name),
            alpha=0.96,
            zorder=3,
        )

    ax.set_xlabel(_design_metric_ylabel(metric), fontsize=12.5, color=DESIGN_INK, labelpad=12)
    ax.set_ylabel("")
    ax.set_yticks(list(variant_positions.values()))
    ax.set_yticklabels([_design_variant_label(variant) for variant in variants])
    ax.invert_yaxis()
    _set_design_interval_xlim(ax, summary, metric)
    _apply_design_axis_style(ax, grid_axis="x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.legend(
        title="Модель",
        loc="upper right",
        bbox_to_anchor=(1.0, 1.18),
        frameon=False,
        ncol=len(models),
        fontsize=11,
        title_fontsize=11,
        labelcolor=DESIGN_INK,
    )
    _add_design_footer(fig, "Интервалы рассчитаны тем же методом, что и в исходных графиках.")
    fig.subplots_adjust(left=0.20, right=0.88, top=0.78, bottom=0.17)
    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def _plot_design_token_breakdown(
    frame: pd.DataFrame,
    output_path: Path,
    coverage_ratio: float,
) -> None:
    if frame.empty:
        return

    summary = summarize_token_records(frame)
    if summary.empty:
        return

    fig, ax = _setup_design_figure()
    _add_design_header(
        fig,
        "Completion-токены по порядку действий",
        f"Столбец — среднее число completion-токенов. Покрытие выборки {coverage_ratio:.0%}.",
    )

    width = 0.74 / max(len(MODEL_NAMES), 1)
    variant_positions = list(range(len(VARIANT_NAMES)))
    max_height = 0.0
    model_handles = []

    for model_index, model_name in enumerate(MODEL_NAMES):
        color = DESIGN_COLORS[model_index % len(DESIGN_COLORS)]
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
        ax.bar(
            x_positions,
            reasoning_values,
            width=width * 0.88,
            color=color,
            alpha=0.96,
            edgecolor="none",
        )
        ax.bar(
            x_positions,
            raw_values,
            width=width * 0.88,
            bottom=reasoning_values,
            color=color,
            alpha=0.40,
            edgecolor="none",
        )
        max_height = max(max_height, *(total_values or [0.0]))
        model_handles.append(Patch(facecolor=color, alpha=0.96, label=_design_model_label(model_name)))

    ax.set_ylabel("Среднее число completion-токенов", fontsize=12.5, color=DESIGN_INK, labelpad=12)
    ax.set_xlabel("")
    ax.set_xticks(variant_positions)
    ax.set_xticklabels([_design_variant_label(variant) for variant in VARIANT_NAMES])
    ax.set_ylim(0, max_height * 1.16 if max_height > 0 else 1.0)
    _apply_design_axis_style(ax, grid_axis="y")

    model_legend = ax.legend(
        handles=model_handles,
        title="Модель",
        loc="upper right",
        bbox_to_anchor=(1.0, 1.18),
        frameon=False,
        ncol=len(MODEL_NAMES),
        fontsize=11,
        title_fontsize=11,
        labelcolor=DESIGN_INK,
    )
    ax.add_artist(model_legend)
    ax.legend(
        handles=[
            Patch(facecolor=DESIGN_INK, alpha=0.96, label="reasoning"),
            Patch(facecolor=DESIGN_INK, alpha=0.40, label="raw answer"),
        ],
        title="Тип токенов",
        loc="upper right",
        bbox_to_anchor=(1.0, 1.08),
        frameon=False,
        ncol=2,
        fontsize=10.5,
        title_fontsize=10.5,
        labelcolor=DESIGN_INK,
    )
    _add_design_footer(fig, "Сводка по всем задачам и запускам.")
    fig.subplots_adjust(left=0.10, right=0.96, top=0.76, bottom=0.20)
    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


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
    ax.set_ylabel(_metric_ylabel(metric), fontsize=11, color="#555555")
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
    ax.set_ylabel(_metric_ylabel(metric), fontsize=11, color="#555555")
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


def _confidence_interval_table(records: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict] = []
    if records.empty:
        return pd.DataFrame(rows, columns=CONFIDENCE_INTERVAL_COLUMNS)

    for metric in METRICS:
        metric_records = _metric_subset(records, metric)
        if metric_records.empty:
            continue
        coverage_ratio = len(metric_records) / len(records)
        summary = summarize_confidence_intervals(metric_records, metric, coverage_ratio)
        rows.extend(summary.to_dict("records"))

    return pd.DataFrame(rows, columns=CONFIDENCE_INTERVAL_COLUMNS)


def _write_confidence_interval_table(records: pd.DataFrame, output_path: Path) -> None:
    table = _confidence_interval_table(records)
    if table.empty:
        return
    table.to_csv(output_path, index=False)


def build_reports(domains: list[str], problem_refs: list[ProblemRef]) -> None:
    all_records = build_records(domains, problem_refs)

    for domain_name in domains:
        domain_records = all_records[all_records["domain"] == domain_name].copy()
        graph_dir = Path("materials") / domain_name / "graph"
        if graph_dir.exists():
            shutil.rmtree(graph_dir)
        graph_dir.mkdir(parents=True, exist_ok=True)
        design_dir = graph_dir / DESIGN_GRAPH_DIR_NAME

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
                _plot_confidence_intervals(
                    metric_records,
                    metric,
                    problem_dir / f"{metric['slug']}_confidence_intervals.png",
                    f"{CONFIDENCE_LEVEL_LABEL} CI: {_metric_title(metric, coverage_ratio)} - {problem_label}",
                )

            _write_confidence_interval_table(problem_records, problem_dir / "confidence_intervals.csv")

            token_records = _token_breakdown_subset(problem_records)
            token_coverage_ratio = len(token_records) / len(problem_records)
            _plot_problem_token_breakdown(
                token_records,
                problem_dir / "completion_token_breakdown_barplot.png",
                f"{_token_breakdown_title(token_coverage_ratio)} by variant - {problem_label}",
            )

        if domain_records.empty:
            continue

        for metric in METRICS:
            metric_records = _metric_subset(domain_records, metric)
            if metric_records.empty:
                continue

            coverage_ratio = len(metric_records) / len(domain_records)
            _plot_problem_variant_bar(
                metric_records,
                metric,
                graph_dir / f"{metric['slug']}_by_order_barplot.png",
                f"{_metric_title(metric, coverage_ratio)} by order",
            )
            _plot_confidence_intervals(
                metric_records,
                metric,
                graph_dir / f"{metric['slug']}_by_order_confidence_intervals.png",
                f"{CONFIDENCE_LEVEL_LABEL} CI: {_metric_title(metric, coverage_ratio)} by order",
            )
            _plot_design_order_bar(
                metric_records,
                metric,
                _design_output_path(design_dir, f"{metric['slug']}_by_order_barplot.png"),
                coverage_ratio,
            )
            _plot_design_confidence_intervals(
                metric_records,
                metric,
                _design_output_path(design_dir, f"{metric['slug']}_by_order_confidence_intervals.png"),
                coverage_ratio,
            )

        _write_confidence_interval_table(domain_records, graph_dir / "confidence_intervals_by_order.csv")

        token_records = _token_breakdown_subset(domain_records)
        token_coverage_ratio = len(token_records) / len(domain_records)
        _plot_problem_token_breakdown(
            token_records,
            graph_dir / "completion_token_breakdown_by_order_barplot.png",
            f"{_token_breakdown_title(token_coverage_ratio)} by order",
        )
        _plot_design_token_breakdown(
            token_records,
            _design_output_path(design_dir, "completion_token_breakdown_by_order_barplot.png"),
            token_coverage_ratio,
        )
