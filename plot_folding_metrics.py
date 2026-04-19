import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp")

import matplotlib
import pandas as pd
import seaborn as sns

matplotlib.use("Agg")
import matplotlib.pyplot as plt


sns.set_style("whitegrid")
plt.rcParams.update({
    "figure.figsize": (14, 8),
    "axes.titlesize": 18,
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 12,
    "font.family": "sans-serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

MODEL_PALETTE = {
    "gpt-5-mini": "#1f77b4",
    "grok-4-1-fast": "#ff7f0e",
    "mimo-v2-flash": "#2ca02c",
    "qwen3-5-35b-a3b-alibaba": "#d62728",
}


def load_global_metric() -> dict:
    with open("materials/metric.json", encoding="utf-8") as handle:
        return json.load(handle)


def build_records(metric: dict, domains: list[str]) -> pd.DataFrame:
    records: list[dict] = []

    for domain_name in domains:
        for problem_id, variants in metric.get(domain_name, {}).items():
            for variant_name, summary in variants.items():
                strict_summary = summary.get("strict_summary", {})
                legacy_summary = summary.get("legacy_summary", {})
                order_summary = summary.get("order_summary", {})
                model_names = set(strict_summary) | set(legacy_summary) | set(order_summary)

                for model_name in sorted(model_names):
                    strict = strict_summary.get(model_name, {})
                    legacy = legacy_summary.get(model_name, {})
                    order = order_summary.get(model_name, {})

                    records.append({
                        "domain": domain_name,
                        "problem": problem_id,
                        "variant": variant_name,
                        "model": model_name,
                        "parsable": strict.get("parsable"),
                        "executability": strict.get("executability"),
                        "reachability": strict.get("reachability"),
                        "first_failure_step": strict.get("first_failure_step"),
                        "non_executable_failure": strict.get("non_executable_failure"),
                        "strict_final_value": strict.get("strict_final_value"),
                        "legacy_cost": legacy.get("cost"),
                        "legacy_gap": legacy.get("gap"),
                        "bug_optimal": legacy.get("bug_optimal"),
                        "optimality_ratio": legacy.get("optimality_ratio"),
                        "order_distance_norm": order.get("normalized_distance"),
                    })

    return pd.DataFrame(records)


def _rate_barplot(data: pd.DataFrame, value_column: str, title: str, output_path: Path) -> None:
    if data.empty:
        return

    plt.figure()
    sns.barplot(data=data, x="variant", y=value_column, hue="model", palette=MODEL_PALETTE)
    plt.title(title, pad=20)
    plt.xlabel("Variant")
    plt.ylabel("Rate (%)")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Model", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def _value_barplot(data: pd.DataFrame, value_column: str, title: str, ylabel: str, output_path: Path) -> None:
    if data.empty:
        return

    plt.figure()
    sns.barplot(data=data, x="variant", y=value_column, hue="model", palette=MODEL_PALETTE)
    plt.title(title, pad=20)
    plt.xlabel("Variant")
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Model", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def write_domain_report(domain_name: str, records: pd.DataFrame, output_path: Path) -> None:
    overall = records.groupby("model").agg(
        executability_rate=("executability", "mean"),
        reachability_rate=("reachability", "mean"),
        mean_order_distance=("order_distance_norm", "mean"),
    ).reset_index()

    executable = records[records["executability"] == True]
    if not executable.empty:
        conditional = executable.groupby("model")["reachability"].mean().rename("conditional_reachability")
        overall = overall.merge(conditional, on="model", how="left")
    else:
        overall["conditional_reachability"] = None

    goal_reaching = records[records["reachability"] == True]
    if not goal_reaching.empty:
        ratios = goal_reaching.groupby("model")["optimality_ratio"].mean().rename("mean_optimality_ratio")
        overall = overall.merge(ratios, on="model", how="left")
    else:
        overall["mean_optimality_ratio"] = None

    non_executable = records[records["executability"] == False].copy()
    if not non_executable.empty:
        non_executable["parse_error_share"] = non_executable["non_executable_failure"] == "parse_error"
        non_executable["state_execution_error_share"] = non_executable["non_executable_failure"] == "state_execution_error"
        failure_rates = non_executable.groupby("model").agg(
            parse_error_share=("parse_error_share", "mean"),
            state_execution_error_share=("state_execution_error_share", "mean"),
        ).reset_index()
        overall = overall.merge(failure_rates, on="model", how="left")
    else:
        overall["parse_error_share"] = None
        overall["state_execution_error_share"] = None

    table_lines = [
        "| model | executability_rate | reachability_rate | mean_order_distance | conditional_reachability | mean_optimality_ratio | parse_error_share | state_execution_error_share |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in overall.to_dict(orient="records"):
        formatted_row = {}
        for key, value in row.items():
            if pd.isna(value):
                formatted_row[key] = "null"
            elif isinstance(value, float):
                formatted_row[key] = f"{value:.4f}"
            else:
                formatted_row[key] = value
        table_lines.append(
            "| {model} | {executability_rate} | {reachability_rate} | {mean_order_distance} | {conditional_reachability} | {mean_optimality_ratio} | {parse_error_share} | {state_execution_error_share} |".format(
                **formatted_row
            )
        )

    lines = [
        f"# {domain_name} report",
        "",
        f"Plans covered: {len(records)}",
        "",
        *table_lines,
        "",
    ]
    output_path.write_text("\n".join(lines), encoding="utf-8")


def build_report_for_domain(domain_name: str, records: pd.DataFrame) -> None:
    if records.empty:
        print(f"skip {domain_name}: no aggregated records")
        return

    graph_dir = Path("materials") / domain_name / "graph"
    graph_dir.mkdir(parents=True, exist_ok=True)

    executability = records.groupby(["variant", "model"])["executability"].mean().mul(100).reset_index()
    reachability = records.groupby(["variant", "model"])["reachability"].mean().mul(100).reset_index()

    executable = records[records["executability"] == True]
    conditional = pd.DataFrame(columns=["variant", "model", "reachability"])
    if not executable.empty:
        conditional = executable.groupby(["variant", "model"])["reachability"].mean().mul(100).reset_index()

    goal_reaching = records[records["reachability"] == True]
    optimality = pd.DataFrame(columns=["variant", "model", "optimality_ratio"])
    if not goal_reaching.empty:
        optimality = goal_reaching.groupby(["variant", "model"])["optimality_ratio"].mean().reset_index()

    non_executable = records[records["executability"] == False].copy()
    parse_error = pd.DataFrame(columns=["variant", "model", "parse_error_share"])
    state_execution_error = pd.DataFrame(columns=["variant", "model", "state_execution_error_share"])
    if not non_executable.empty:
        non_executable["parse_error_share"] = non_executable["non_executable_failure"] == "parse_error"
        non_executable["state_execution_error_share"] = non_executable["non_executable_failure"] == "state_execution_error"
        parse_error = non_executable.groupby(["variant", "model"])["parse_error_share"].mean().mul(100).reset_index()
        state_execution_error = non_executable.groupby(["variant", "model"])["state_execution_error_share"].mean().mul(100).reset_index()

    _rate_barplot(
        executability,
        "executability",
        f"Executability Rate by Variant and Model — {domain_name}",
        graph_dir / "executability_rate_by_variant_model.png",
    )
    _rate_barplot(
        reachability,
        "reachability",
        f"Reachability Rate by Variant and Model — {domain_name}",
        graph_dir / "reachability_rate_by_variant_model.png",
    )
    _rate_barplot(
        conditional,
        "reachability",
        f"Conditional Reachability by Variant and Model — {domain_name}",
        graph_dir / "conditional_reachability_by_variant_model.png",
    )
    _value_barplot(
        optimality,
        "optimality_ratio",
        f"Mean Optimality Ratio Among Goal-Reaching Plans — {domain_name}",
        "Optimality ratio",
        graph_dir / "mean_optimality_ratio_by_variant_model.png",
    )
    _rate_barplot(
        parse_error,
        "parse_error_share",
        f"Parse Error Share Among Non-Executable Plans — {domain_name}",
        graph_dir / "parse_error_share_by_variant_model.png",
    )
    _rate_barplot(
        state_execution_error,
        "state_execution_error_share",
        f"State Execution Error Share Among Non-Executable Plans — {domain_name}",
        graph_dir / "state_execution_error_share_by_variant_model.png",
    )

    write_domain_report(domain_name, records, Path("materials") / domain_name / "report.md")
    print(f"report artifacts written for {domain_name}")


def build_reports_for_domains(domains: list[str]) -> None:
    metric = load_global_metric()
    records = build_records(metric, domains)

    for domain_name in domains:
        build_report_for_domain(domain_name, records[records["domain"] == domain_name].copy())


if __name__ == "__main__":
    metric = load_global_metric()
    build_reports_for_domains(list(metric.keys()))
