from pathlib import Path
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_all_metrics(domain: str = "folding"):
    metric_path = Path(f"materials/{domain}/metric.json")
    if not metric_path.exists():
        print("❌ metric.json не найден")
        return None
    with open(metric_path, encoding='utf-8') as f:
        data = json.load(f)
    return data.get(domain, {})

def create_summary_table(metrics_dict):
    rows = []
    for prob, variants in metrics_dict.items():
        for variant, models in variants.items():
            for model, stats in models.items():
                rows.append({
                    "problem": prob,
                    "variant": variant,
                    "model": model,
                    "valid": stats["valid"],
                    "llm_cost": stats["llm_cost"],
                    "optimal_cost": stats["optimal_cost"],
                    "gap_%": stats["cost_gap_%"],
                    "bug_optimal": stats["bug_optimal"],
                    "order_dist": stats["order_distance_norm"],
                    "duration": stats["duration_sec"],
                    "tokens": stats["total_tokens"]
                })
    df = pd.DataFrame(rows)
    return df

def plot_results(domain: str = "folding"):
    data = load_all_metrics(domain)
    if not data:
        return

    df = create_summary_table(data)

    # Основная таблица
    print("\n📊 СВОДНАЯ ТАБЛИЦА ПО МОДЕЛЯМ (средние значения)")
    summary = df.groupby("model").agg({
        "valid": "mean",
        "gap_%": "mean",
        "bug_optimal": "sum",
        "order_dist": "mean",
        "duration": "mean",
        "tokens": "mean"
    }).round(3)
    print(summary)

    # Графики
    plt.figure(figsize=(14, 8))

    # 1. Bug-optimal по вариантам
    plt.subplot(2, 2, 1)
    bug = df.groupby(["variant", "model"])["bug_optimal"].sum().unstack()
    bug.plot(kind="bar", ax=plt.gca())
    plt.title("Bug-optimal (сколько раз модель нашла loophole)")
    plt.ylabel("Количество")
    plt.xticks(rotation=45)

    # 2. Средний GAP
    plt.subplot(2, 2, 2)
    sns.barplot(data=df, x="model", y="gap_%", hue="variant")
    plt.title("Средний GAP% (отрицательный = лучше оптимального)")
    plt.xticks(rotation=45)

    # 3. Время выполнения
    plt.subplot(2, 2, 3)
    sns.boxplot(data=df, x="model", y="duration")
    plt.title("Время выполнения (сек)")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig(f"materials/{domain}_results.png", dpi=300, bbox_inches="tight")
    plt.show()

    # Сохраняем CSV
    df.to_csv(f"materials/{domain}_full_results.csv", index=False)
    print(f"✅ Графики и CSV сохранены: materials/{domain}_results.png и {domain}_full_results.csv")

if __name__ == "__main__":
    plot_results("folding")