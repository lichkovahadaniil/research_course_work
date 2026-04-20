import os
import shutil
import json
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp")

import matplotlib
import pandas as pd
from matplotlib.ticker import PercentFormatter

from manual_model_run import model_output_dir_name
from shuffler import VARIANT_NAMES


matplotlib.use("Agg")
import matplotlib.pyplot as plt


MODEL_NAMES = [
    "gpt-5-mini",
    "grok-4-1-fast",
    "qwen3-5-35b-a3b-alibaba",
]
RECORD_COLUMNS = [
    "domain",
    "problem",
    "variant",
    "model",
    "plan_length",
    "executability",
    "reachability",
    "conditional_reachability",
    "optimality_ratio",
    "first_failure_step",
    "non_executable_failure",
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

# Современная палитра цветов для трех моделей (Синий, Оранжевый, Зеленый)
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
        if height > 0.001:  # Не пишем ничего над пустыми столбцами
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
            
def build_records(domains: list[str], problem_ids: list[str]) -> pd.DataFrame:
    records: list[dict] = []

    for domain_name in domains:
        for problem_id in problem_ids:
            problem_dir = Path("materials") / domain_name / problem_id
            for variant_name in VARIANT_NAMES:
                variant_dir = problem_dir / variant_name
                for model_name in MODEL_NAMES:
                    result_path = variant_dir / model_output_dir_name(model_name) / "llm_result.json"
                    if not result_path.exists():
                        continue

                    payload = _load_result(result_path)
                    metrics = payload.get("metrics") or {}
                    strict = metrics.get("strict") or {}
                    legacy = metrics.get("legacy") or {}

                    executability = bool(strict.get("executability"))
                    reachability = bool(strict.get("reachability"))

                    records.append(
                        {
                            "domain": domain_name,
                            "problem": problem_id,
                            "variant": variant_name,
                            "model": model_name,
                            "plan_length": strict.get("plan_length") if reachability else None,
                            "executability": float(executability),
                            "reachability": float(reachability),
                            "conditional_reachability": float(executability and reachability),
                            "optimality_ratio": legacy.get("optimality_ratio") if reachability else None,
                            "first_failure_step": strict.get("first_failure_step"),
                            "non_executable_failure": float(strict.get("non_executable_failure") is not None),
                        }
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


def _plot_problem_average_bar(frame: pd.DataFrame, metric: dict, output_path: Path, title: str) -> None:
    if frame.empty:
        return

    avg_series = frame.groupby("model")[metric["slug"]].mean().reindex(MODEL_NAMES).fillna(0)

    ax = avg_series.plot(
        kind="bar", 
        width=0.6, 
        figsize=(8, 6),
        color=MODERN_COLORS,
        edgecolor="none" # Убираем черную обводку самих столбцов
    )
    
    ax.set_title(title, pad=20, fontsize=14, fontweight='bold', color='#333333')
    ax.set_ylabel(f"Average {metric['title']}", fontsize=11, color='#555555')
    ax.set_xlabel("Model", fontsize=11, color='#555555')
    
    _apply_modern_style(ax)
    _add_value_labels(ax, is_rate=metric["rate"])
    
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


def _plot_summary_bar(frame: pd.DataFrame, metric: dict, output_path: Path, title: str) -> None:
    if frame.empty:
        return

    avg_frame = frame.groupby(["variant", "model"])[metric["slug"]].mean().reset_index()
    
    pivot = (
        avg_frame.pivot(index="variant", columns="model", values=metric["slug"])
        .reindex(index=VARIANT_NAMES, columns=MODEL_NAMES)
        .fillna(0)
    )

    ax = pivot.plot(
        kind="bar", 
        width=0.8, 
        figsize=(12, 6), # Сделали чуть шире для summary
        color=MODERN_COLORS,
        edgecolor="none"
    )
    
    ax.set_title(title, pad=20, fontsize=14, fontweight='bold', color='#333333')
    ax.set_ylabel(f"Average {metric['title']}", fontsize=11, color='#555555')
    ax.set_xlabel("Domain Variant", fontsize=11, color='#555555')
    
    _apply_modern_style(ax)
    _add_value_labels(ax, is_rate=metric["rate"])
    
    # Красивая легенда без страшной белой рамки
    ax.legend(title="Models", bbox_to_anchor=(1.02, 1), loc='upper left', frameon=False, title_fontsize='12')
    
    if metric["rate"]:
        ax.set_ylim(0, 1.15)
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
    else:
        ax.set_ylim(0, ax.get_ylim()[1] * 1.15)
    
    plt.xticks(rotation=45, ha='right', color='#333333') # ha='right' чтобы подписи не съезжали
    plt.yticks(color='#333333')
    plt.tight_layout()
    
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def build_reports(domains: list[str], problem_ids: list[str]) -> None:
    all_records = build_records(domains, problem_ids)

    for domain_name in domains:
        domain_records = all_records[all_records["domain"] == domain_name].copy()
        graph_dir = Path("materials") / domain_name / "graph"
        if graph_dir.exists():
            shutil.rmtree(graph_dir)
        graph_dir.mkdir(parents=True, exist_ok=True)

        for problem_id in problem_ids:
            (graph_dir / problem_id).mkdir(parents=True, exist_ok=True)
        summary_dir = graph_dir / "summary"
        summary_dir.mkdir(parents=True, exist_ok=True)

        total_expected = len(problem_ids) * len(VARIANT_NAMES) * len(MODEL_NAMES)

        # Рисуем графики для каждой конкретной проблемы (усредненно по перемешиваниям)
        for problem_id in problem_ids:
            problem_records = domain_records[domain_records["problem"] == problem_id].copy()
            problem_dir = graph_dir / problem_id

            for metric in METRICS:
                metric_records = _metric_subset(problem_records, metric)
                _plot_problem_average_bar( # Используем первую функцию
                    metric_records,
                    metric,
                    problem_dir / f"{metric['slug']}_barplot.png",
                    f"Average {metric['title']} across variants - {problem_id}",
                )

        # Рисуем сводные графики (усредненно по проблемам)
        for metric in METRICS:
            metric_records = _metric_subset(domain_records, metric)
            _plot_summary_bar( # Используем вторую функцию
                metric_records, 
                metric,
                summary_dir / f"{metric['slug']}_summary_barplot.png",
                f"Overall Average {metric['title']} by Variant"
            )
