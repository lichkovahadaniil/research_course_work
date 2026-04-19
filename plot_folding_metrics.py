import json
import os
from pathlib import Path
from typing import Any

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp")

import matplotlib
from matplotlib.colors import ListedColormap
from matplotlib.ticker import PercentFormatter
import pandas as pd
import seaborn as sns

matplotlib.use("Agg")
import matplotlib.pyplot as plt


sns.set_style("whitegrid")
plt.rcParams.update({
    "figure.figsize": (12, 6),
    "axes.titlesize": 16,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "font.family": "sans-serif",
})

MODEL_ORDER = [
    "gpt-5-mini",
    "grok-4-1-fast",
    "mimo-v2-flash",
    "qwen3-5-35b-a3b-alibaba",
]
VARIANT_ORDER = [
    "canonical",
    "optimal",
    "frequency",
    "dispersion",
    "random_01",
    "random_02",
    "random_03",
    "random_04",
    "random_05",
]
NON_EXECUTABLE_CODES = {
    "parse_error": 1,
    "state_execution_error": 2,
    "validator_timeout": 3,
}
NON_EXECUTABLE_LABELS = {
    "parse_error": "parse",
    "state_execution_error": "state",
    "validator_timeout": "timeout",
}
METRIC_SPECS = [
    {
        "slug": "plan_length",
        "title": "Plan Length",
        "problem_column": "plan_length_metric",
        "summary_column": "plan_length_metric",
        "problem_kind": "int",
        "summary_kind": "float",
        "problem_cmap": "Blues",
        "summary_cmap": "Blues",
    },
    {
        "slug": "executability",
        "title": "Executability",
        "problem_column": "executability",
        "summary_column": "executability",
        "problem_kind": "bool",
        "summary_kind": "rate",
        "problem_cmap": "Greens",
        "summary_cmap": "Greens",
    },
    {
        "slug": "reachability",
        "title": "Reachability",
        "problem_column": "reachability",
        "summary_column": "reachability",
        "problem_kind": "bool",
        "summary_kind": "rate",
        "problem_cmap": "Greens",
        "summary_cmap": "Greens",
    },
    {
        "slug": "conditional_reachability",
        "title": "Conditional Reachability",
        "problem_column": "conditional_reachability",
        "summary_column": "conditional_reachability",
        "problem_kind": "bool",
        "summary_kind": "rate",
        "problem_cmap": "Greens",
        "summary_cmap": "Greens",
    },
    {
        "slug": "first_failure_step",
        "title": "First Failure Step",
        "problem_column": "first_failure_step",
        "summary_column": "first_failure_step",
        "problem_kind": "int",
        "summary_kind": "float",
        "problem_cmap": "Oranges",
        "summary_cmap": "Oranges",
    },
    {
        "slug": "optimality_ratio",
        "title": "Optimality Ratio",
        "problem_column": "optimality_ratio",
        "summary_column": "optimality_ratio",
        "problem_kind": "float",
        "summary_kind": "float",
        "problem_cmap": "Blues",
        "summary_cmap": "Blues",
    },
    {
        "slug": "non_executable_failure",
        "title": "Non-Executable Failure",
        "problem_column": "non_executable_failure",
        "summary_column": "non_executable_failure_parse_share",
        "problem_kind": "category",
        "summary_kind": "rate",
        "problem_cmap": None,
        "summary_cmap": "Reds",
    },
]


def load_json(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def load_metric_metadata() -> dict[str, Any]:
    metric_path = Path("materials/metric.json")
    if not metric_path.exists():
        return {}

    try:
        payload = load_json(metric_path)
    except json.JSONDecodeError:
        return {}

    metadata = payload.get("_meta")
    return metadata if isinstance(metadata, dict) else {}


def resolve_problem_filters(
    domains: list[str],
    explicit_problem_ids: list[str] | None = None,
) -> dict[str, list[str] | None]:
    if explicit_problem_ids is not None:
        return {domain_name: explicit_problem_ids[:] for domain_name in domains}

    metadata = load_metric_metadata()
    domains_meta = metadata.get("domains", {}) if isinstance(metadata.get("domains"), dict) else {}

    problem_filters: dict[str, list[str] | None] = {}
    for domain_name in domains:
        selected = domains_meta.get(domain_name, {}).get("selected_problems")
        if isinstance(selected, list) and selected:
            problem_filters[domain_name] = selected[:]
        else:
            problem_filters[domain_name] = None
    return problem_filters


def model_sort_key(model_name: str) -> tuple[int, str]:
    return (MODEL_ORDER.index(model_name), model_name) if model_name in MODEL_ORDER else (len(MODEL_ORDER), model_name)


def variant_sort_key(variant_name: str) -> tuple[int, str]:
    return (VARIANT_ORDER.index(variant_name), variant_name) if variant_name in VARIANT_ORDER else (len(VARIANT_ORDER), variant_name)


def domain_variant_sort_key(label: str) -> tuple[str, int, str]:
    if " / " not in label:
        return (label, len(VARIANT_ORDER), "")

    domain_name, variant_name = label.split(" / ", 1)
    variant_index, variant_fallback = variant_sort_key(variant_name)
    return (domain_name, variant_index, variant_fallback)


def iter_variant_dirs(domain_name: str, problem_ids: list[str] | None = None) -> list[Path]:
    domain_path = Path("materials") / domain_name
    selected = set(problem_ids) if problem_ids is not None else None
    variant_dirs: list[Path] = []

    for problem_dir in sorted((path for path in domain_path.glob("p*") if path.is_dir()), key=lambda path: path.name):
        if selected is not None and problem_dir.name not in selected:
            continue
        for variant_dir in sorted(
            (child for child in problem_dir.iterdir() if child.is_dir() and (child / "domain.pddl").exists()),
            key=lambda path: variant_sort_key(path.name),
        ):
            if (variant_dir / "llm_summary.json").exists():
                variant_dirs.append(variant_dir)
    return variant_dirs


def build_records(
    domains: list[str],
    problem_ids: list[str] | None = None,
    problem_filters: dict[str, list[str] | None] | None = None,
) -> pd.DataFrame:
    records: list[dict[str, Any]] = []

    for domain_name in domains:
        selected_problem_ids = problem_ids
        if problem_filters is not None:
            selected_problem_ids = problem_filters.get(domain_name)

        for variant_dir in iter_variant_dirs(domain_name, problem_ids=selected_problem_ids):
            summary = load_json(variant_dir / "llm_summary.json")
            metrics_payload = load_json(variant_dir / "llm_metrics.json") if (variant_dir / "llm_metrics.json").exists() else {}
            results_by_model = metrics_payload.get("results_by_model", {})

            strict_summary = summary.get("strict_summary", {})
            legacy_summary = summary.get("legacy_summary", {})
            order_summary = summary.get("order_summary", {})
            model_names = sorted(
                set(strict_summary) | set(legacy_summary) | set(order_summary) | set(results_by_model),
                key=model_sort_key,
            )

            for model_name in model_names:
                strict = strict_summary.get(model_name, {})
                legacy = legacy_summary.get(model_name, {})
                order = order_summary.get(model_name, {})
                runtime = results_by_model.get(model_name, {})
                full_metrics = runtime.get("metrics") or {}
                reference = full_metrics.get("reference") or {}
                deprecated = order.get("deprecated_action_name_distance") or {}

                parsable = strict.get("parsable")
                executability = strict.get("executability")
                reachability = strict.get("reachability")
                failure_type = strict.get("non_executable_failure")

                records.append({
                    "domain": domain_name,
                    "problem": summary.get("problem", variant_dir.parent.name),
                    "variant": summary.get("variant", variant_dir.name),
                    "model": model_name,
                    "parsable": parsable,
                    "executability": executability,
                    "reachability": reachability,
                    "conditional_reachability": reachability if executability else None,
                    "plan_length": strict.get("plan_length"),
                    "plan_length_metric": strict.get("plan_length") if parsable else None,
                    "first_failure_step": strict.get("first_failure_step"),
                    "strict_final_value": strict.get("strict_final_value"),
                    "non_executable_failure": failure_type,
                    "non_executable_failure_parse_share": (
                        1.0 if failure_type == "parse_error"
                        else 0.0 if failure_type in {"state_execution_error", "validator_timeout"}
                        else None
                    ),
                    "parse_error_flag": failure_type == "parse_error",
                    "state_execution_error_flag": failure_type == "state_execution_error",
                    "validator_timeout_flag": failure_type == "validator_timeout",
                    "legacy_cost": legacy.get("cost"),
                    "legacy_gap": legacy.get("gap"),
                    "bug_optimal": legacy.get("bug_optimal"),
                    "optimality_ratio": legacy.get("optimality_ratio"),
                    "optimal_cost": legacy.get("optimal_cost") or reference.get("optimal_cost"),
                    "optimal_plan_length": reference.get("optimal_plan_length"),
                    "matching_actions": order.get("matching_actions"),
                    "insertions": order.get("insertions"),
                    "deletions": order.get("deletions"),
                    "total_distance": order.get("total_distance"),
                    "normalized_distance": order.get("normalized_distance"),
                    "llm_actions_count": order.get("llm_actions_count"),
                    "optimal_actions_count": order.get("optimal_actions_count"),
                    "deprecated_kendall_tau_inversions": deprecated.get("kendall_tau_inversions"),
                    "deprecated_insertions": deprecated.get("insertions"),
                    "deprecated_deletions": deprecated.get("deletions"),
                    "deprecated_total_distance": deprecated.get("total_distance"),
                    "deprecated_normalized_distance": deprecated.get("normalized_distance"),
                    "reasoning_enabled": runtime.get("reasoning_enabled"),
                    "duration_sec": runtime.get("duration_sec"),
                    "prompt_tokens": runtime.get("prompt_tokens"),
                    "completion_tokens": runtime.get("completion_tokens"),
                    "total_tokens": runtime.get("total_tokens"),
                })

    return pd.DataFrame(records)


def ordered_problem_frame(records: pd.DataFrame) -> pd.DataFrame:
    if records.empty:
        return records.copy()

    return records.sort_values(
        by=["variant", "model"],
        key=lambda column: column.map(lambda value: variant_sort_key(value) if column.name == "variant" else model_sort_key(value)),
    ).reset_index(drop=True)


def write_problem_csv(problem_records: pd.DataFrame, output_path: Path) -> None:
    frame = ordered_problem_frame(problem_records)
    frame.to_csv(output_path, index=False)


def write_problem_markdown(problem_id: str, problem_records: pd.DataFrame) -> list[str]:
    column_order = [
        ("variant", "variant"),
        ("model", "model"),
        ("parsable", "parsable"),
        ("plan_length_metric", "plan_length"),
        ("executability", "executability"),
        ("reachability", "reachability"),
        ("conditional_reachability", "conditional_reachability"),
        ("first_failure_step", "first_failure_step"),
        ("optimality_ratio", "optimality_ratio"),
        ("non_executable_failure", "non_executable_failure"),
    ]

    selected_columns = [column for column, _ in column_order]
    rows = ordered_problem_frame(problem_records)[selected_columns].to_dict(orient="records")
    header = [label for _, label in column_order]
    lines = [
        f"## {problem_id}",
        "",
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * len(header)) + " |",
    ]

    for row in rows:
        formatted_values: list[str] = []
        for column_name, _label in column_order:
            value = row[column_name]
            if pd.isna(value):
                formatted_values.append("null")
            elif isinstance(value, bool):
                formatted_values.append("1" if value else "0")
            elif isinstance(value, float):
                formatted_values.append(f"{value:.4f}")
            else:
                formatted_values.append(str(value))
        lines.append("| " + " | ".join(formatted_values) + " |")

    lines.append("")
    return lines


def cleanup_generated_artifacts(output_dir: Path, expected_filenames: set[str]) -> None:
    if not output_dir.exists():
        return

    for child in output_dir.iterdir():
        if child.is_file() and child.name not in expected_filenames and child.suffix in {".png", ".csv"}:
            child.unlink()


def pivot_metric(records: pd.DataFrame, column: str, index: str = "variant", columns: str = "model") -> pd.DataFrame:
    pivot = records.pivot(index=index, columns=columns, values=column)

    if index == "variant":
        ordered_index = [item for item in VARIANT_ORDER if item in pivot.index] + sorted(set(pivot.index) - set(VARIANT_ORDER))
    elif index == "domain_variant":
        ordered_index = sorted(pivot.index, key=domain_variant_sort_key)
    else:
        ordered_index = sorted(pivot.index)

    ordered_columns = [item for item in MODEL_ORDER if item in pivot.columns] + sorted(set(pivot.columns) - set(MODEL_ORDER))
    return pivot.reindex(index=ordered_index, columns=ordered_columns)


def format_annotation(value: Any, kind: str) -> str:
    if pd.isna(value):
        return ""
    if kind == "bool":
        return "1" if bool(value) else "0"
    if kind == "int":
        return str(int(value))
    if kind == "rate":
        return f"{float(value):.2f}"
    if kind == "float":
        return f"{float(value):.3f}"
    return str(value)


def frame_map(frame: pd.DataFrame, func) -> pd.DataFrame:
    return frame.apply(lambda column: column.map(func))


def plot_numeric_heatmap(
    title: str,
    pivot: pd.DataFrame,
    spec: dict[str, Any],
    output_path: Path,
    scope: str,
) -> None:
    if pivot.empty:
        return

    values = pivot.apply(pd.to_numeric, errors="coerce")
    if values.isna().all().all():
        return

    kind = spec[f"{scope}_kind"]
    annotations = frame_map(values, lambda value: format_annotation(value, kind))
    mask = values.isna()

    figure_width = max(8, 1.8 * len(values.columns) + 3)
    figure_height = max(4.5, 0.7 * len(values.index) + 2.5)
    plt.figure(figsize=(figure_width, figure_height))

    heatmap_kwargs: dict[str, Any] = {
        "data": values,
        "mask": mask,
        "annot": annotations,
        "fmt": "",
        "linewidths": 0.5,
        "linecolor": "white",
        "cmap": spec[f"{scope}_cmap"],
    }
    if kind in {"bool", "rate"}:
        heatmap_kwargs["vmin"] = 0
        heatmap_kwargs["vmax"] = 1

    ax = sns.heatmap(**heatmap_kwargs)
    ax.set_title(title, pad=16)
    ax.set_xlabel("Model")
    ax.set_ylabel("Variant" if values.index.name == "variant" else "Domain / Variant")
    if kind == "rate" and ax.collections:
        ax.collections[0].colorbar.ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
    plt.xticks(rotation=30, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_path, dpi=240, bbox_inches="tight")
    plt.close()


def plot_category_heatmap(title: str, pivot: pd.DataFrame, output_path: Path) -> None:
    if pivot.empty:
        return

    codes = frame_map(pivot, lambda value: NON_EXECUTABLE_CODES.get(value) if pd.notna(value) else None).apply(pd.to_numeric, errors="coerce")
    if codes.isna().all().all():
        return

    annotations = frame_map(pivot, lambda value: NON_EXECUTABLE_LABELS.get(value, "") if pd.notna(value) else "")
    mask = codes.isna()

    figure_width = max(8, 1.8 * len(codes.columns) + 3)
    figure_height = max(4.5, 0.7 * len(codes.index) + 2.5)
    plt.figure(figsize=(figure_width, figure_height))

    cmap = ListedColormap(["#f6c85f", "#f28e2b", "#e15759"])
    ax = sns.heatmap(
        codes,
        mask=mask,
        annot=annotations,
        fmt="",
        linewidths=0.5,
        linecolor="white",
        cmap=cmap,
        vmin=min(NON_EXECUTABLE_CODES.values()),
        vmax=max(NON_EXECUTABLE_CODES.values()),
        cbar_kws={
            "ticks": list(NON_EXECUTABLE_CODES.values()),
            "label": "Failure type",
        },
    )
    colorbar = ax.collections[0].colorbar
    colorbar.set_ticklabels([NON_EXECUTABLE_LABELS[key] for key in NON_EXECUTABLE_CODES])
    ax.set_title(title, pad=16)
    ax.set_xlabel("Model")
    ax.set_ylabel("Variant")
    plt.xticks(rotation=30, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_path, dpi=240, bbox_inches="tight")
    plt.close()


def group_label_order(labels: pd.Series, group_label_column: str) -> list[str]:
    unique_labels = labels.dropna().unique().tolist()
    if group_label_column == "variant":
        return [item for item in VARIANT_ORDER if item in unique_labels] + sorted(set(unique_labels) - set(VARIANT_ORDER))
    if group_label_column == "domain_variant":
        return sorted(unique_labels, key=domain_variant_sort_key)
    return sorted(unique_labels)


def plot_summary_barplot(
    title: str,
    frame: pd.DataFrame,
    spec: dict[str, Any],
    output_path: Path,
    group_label_column: str,
) -> None:
    plot_frame = frame[[group_label_column, "model", spec["summary_column"]]].copy()
    plot_frame[spec["summary_column"]] = pd.to_numeric(plot_frame[spec["summary_column"]], errors="coerce")
    plot_frame = plot_frame.dropna(subset=[spec["summary_column"]])
    if plot_frame.empty:
        return

    group_order = group_label_order(plot_frame[group_label_column], group_label_column)
    hue_order = [item for item in MODEL_ORDER if item in plot_frame["model"].unique()] + sorted(set(plot_frame["model"].unique()) - set(MODEL_ORDER))

    figure_width = max(10, 1.6 * len(hue_order) + 5)
    figure_height = max(5, 0.75 * len(group_order) + 3)
    plt.figure(figsize=(figure_width, figure_height))

    ax = sns.barplot(
        data=plot_frame,
        x=spec["summary_column"],
        y=group_label_column,
        hue="model",
        order=group_order,
        hue_order=hue_order,
        orient="h",
        palette="Set2",
    )
    ax.set_title(title, pad=16)
    ax.set_xlabel(spec["title"])
    ax.set_ylabel("Variant" if group_label_column == "variant" else "Domain / Variant")
    if spec["summary_kind"] == "rate":
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        ax.set_xlim(0, 1)

    if len(group_order) <= 12:
        for container in ax.containers:
            labels = [format_annotation(bar.get_width(), spec["summary_kind"]) if bar.get_width() == bar.get_width() else "" for bar in container]
            ax.bar_label(container, labels=labels, padding=3, fontsize=9)

    ax.legend(title="Model", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(output_path, dpi=240, bbox_inches="tight")
    plt.close()


def summarize_records(records: pd.DataFrame, group_keys: list[str]) -> pd.DataFrame:
    if records.empty:
        return pd.DataFrame(columns=[*group_keys, *(spec["summary_column"] for spec in METRIC_SPECS), "problems_covered"])

    working = records.copy()
    summary_columns = sorted({spec["summary_column"] for spec in METRIC_SPECS})
    for column in summary_columns:
        working[column] = pd.to_numeric(working[column], errors="coerce")

    grouped = working.groupby(group_keys, dropna=False, sort=False)
    summary = grouped.agg({column: "mean" for column in summary_columns}).reset_index()
    problem_counts = grouped["problem"].nunique().reset_index(name="problems_covered")
    return summary.merge(problem_counts, on=group_keys, how="left")


def build_problem_graphs(domain_name: str, problem_id: str, problem_records: pd.DataFrame) -> Path:
    graph_dir = Path("materials") / domain_name / "graph" / problem_id
    graph_dir.mkdir(parents=True, exist_ok=True)

    expected_files = {f"{spec['slug']}_heatmap.png" for spec in METRIC_SPECS} | {"metrics_table.csv"}
    cleanup_generated_artifacts(graph_dir, expected_files)

    for spec in METRIC_SPECS:
        pivot = pivot_metric(problem_records, spec["problem_column"])
        output_path = graph_dir / f"{spec['slug']}_heatmap.png"
        title = f"{spec['title']} - {domain_name} / {problem_id}"
        if spec["problem_kind"] == "category":
            plot_category_heatmap(title, pivot, output_path)
        else:
            plot_numeric_heatmap(title, pivot, spec, output_path, scope="problem")

    write_problem_csv(problem_records, graph_dir / "metrics_table.csv")
    return graph_dir


def build_domain_summary_graphs(domain_name: str, domain_records: pd.DataFrame, selected_problem_ids: list[str]) -> Path:
    summary_dir = Path("materials") / domain_name / "graph" / "summary"
    summary_dir.mkdir(parents=True, exist_ok=True)

    summary_records = summarize_records(domain_records, ["variant", "model"])
    summary_records = summary_records.sort_values(
        by=["variant", "model"],
        key=lambda column: column.map(lambda value: variant_sort_key(value) if column.name == "variant" else model_sort_key(value)),
    ).reset_index(drop=True)

    expected_files = {
        f"{spec['slug']}_summary_heatmap.png" for spec in METRIC_SPECS
    } | {
        f"{spec['slug']}_summary_barplot.png" for spec in METRIC_SPECS
    } | {"summary_metrics.csv"}
    cleanup_generated_artifacts(summary_dir, expected_files)
    summary_records.to_csv(summary_dir / "summary_metrics.csv", index=False)

    problems_label = ", ".join(selected_problem_ids)
    for spec in METRIC_SPECS:
        pivot = pivot_metric(summary_records, spec["summary_column"])
        plot_numeric_heatmap(
            f"{spec['title']} summary - {domain_name} ({problems_label})",
            pivot,
            spec,
            summary_dir / f"{spec['slug']}_summary_heatmap.png",
            scope="summary",
        )
        plot_summary_barplot(
            f"{spec['title']} summary - {domain_name}",
            summary_records,
            spec,
            summary_dir / f"{spec['slug']}_summary_barplot.png",
            group_label_column="variant",
        )

    return summary_dir


def build_cross_domain_graphs(records: pd.DataFrame) -> Path:
    cross_domain_dir = Path("materials") / "graph" / "cross-domain"
    cross_domain_dir.mkdir(parents=True, exist_ok=True)

    summary_records = summarize_records(records, ["domain", "variant", "model"])
    summary_records["domain_variant"] = summary_records.apply(
        lambda row: f"{row['domain']} / {row['variant']}",
        axis=1,
    )
    summary_records = summary_records.sort_values(
        by=["domain_variant", "model"],
        key=lambda column: column.map(domain_variant_sort_key) if column.name == "domain_variant" else column.map(model_sort_key),
    ).reset_index(drop=True)

    expected_files = {
        f"{spec['slug']}_cross_domain_heatmap.png" for spec in METRIC_SPECS
    } | {
        f"{spec['slug']}_cross_domain_barplot.png" for spec in METRIC_SPECS
    } | {"cross_domain_summary_metrics.csv"}
    cleanup_generated_artifacts(cross_domain_dir, expected_files)
    summary_records.to_csv(cross_domain_dir / "cross_domain_summary_metrics.csv", index=False)

    for spec in METRIC_SPECS:
        pivot = pivot_metric(summary_records, spec["summary_column"], index="domain_variant")
        plot_numeric_heatmap(
            f"{spec['title']} cross-domain summary",
            pivot,
            spec,
            cross_domain_dir / f"{spec['slug']}_cross_domain_heatmap.png",
            scope="summary",
        )
        plot_summary_barplot(
            f"{spec['title']} cross-domain summary",
            summary_records,
            spec,
            cross_domain_dir / f"{spec['slug']}_cross_domain_barplot.png",
            group_label_column="domain_variant",
        )

    return cross_domain_dir


def write_domain_report(domain_name: str, records: pd.DataFrame, problem_ids: list[str]) -> None:
    output_path = Path("materials") / domain_name / "report.md"
    lines = [
        f"# {domain_name} report",
        "",
        f"Problems covered in summary: {', '.join(problem_ids)}",
        "",
        f"Per-problem graphs are stored under `materials/{domain_name}/graph/<problem>/`.",
        f"Domain summary graphs are stored under `materials/{domain_name}/graph/summary/`.",
        "",
    ]

    for problem_id in problem_ids:
        problem_records = records[records["problem"] == problem_id].copy()
        if problem_records.empty:
            continue
        lines.extend(write_problem_markdown(problem_id, problem_records))

    output_path.write_text("\n".join(lines), encoding="utf-8")


def build_reports_for_domains(domains: list[str], problem_ids: list[str] | None = None) -> None:
    problem_filters = resolve_problem_filters(domains, explicit_problem_ids=problem_ids)
    records = build_records(domains, problem_filters=problem_filters)
    if records.empty:
        print("no aggregated records found for plotting")
        return

    rendered_domains: list[str] = []

    for domain_name in domains:
        domain_records = records[records["domain"] == domain_name].copy()
        if domain_records.empty:
            print(f"skip {domain_name}: no aggregated records")
            continue

        available_problem_ids = sorted(domain_records["problem"].dropna().unique())
        requested_problem_ids = problem_filters.get(domain_name)
        if requested_problem_ids is None:
            selected_problem_ids = available_problem_ids
        else:
            selected_problem_ids = [problem_id for problem_id in requested_problem_ids if problem_id in set(available_problem_ids)]

        for problem_id in selected_problem_ids:
            problem_records = domain_records[domain_records["problem"] == problem_id].copy()
            graph_dir = build_problem_graphs(domain_name, problem_id, problem_records)
            print(f"graph set written for {domain_name}/{problem_id} -> {graph_dir}")

        summary_dir = build_domain_summary_graphs(domain_name, domain_records, selected_problem_ids)
        print(f"domain summary written for {domain_name} -> {summary_dir}")

        write_domain_report(domain_name, domain_records, selected_problem_ids)
        print(f"report artifacts written for {domain_name}")
        rendered_domains.append(domain_name)

    cross_domain_records = records[records["domain"].isin(rendered_domains)].copy()
    if not cross_domain_records.empty:
        cross_domain_dir = build_cross_domain_graphs(cross_domain_records)
        print(f"cross-domain summary written -> {cross_domain_dir}")


if __name__ == "__main__":
    domains = [path.name for path in Path("materials").iterdir() if path.is_dir()]
    build_reports_for_domains(domains)
