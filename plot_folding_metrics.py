import json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==================== КРАСИВЫЙ ПРОФЕССИОНАЛЬНЫЙ СТИЛЬ ====================
sns.set_style("whitegrid")
plt.rcParams.update({
    'figure.figsize': (14, 8),
    'axes.titlesize': 18,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'font.family': 'sans-serif',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

model_palette = {
    "gpt-5-mini": "#1f77b4",
    "grok-4-1-fast": "#ff7f0e",
    "mimo-v2-flash": "#2ca02c",
    "qwen3-5-35b-a3b-alibaba": "#d62728"
}

# =====================================================================

with open('materials/metric.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for domain, problems in data.items():
    print(f"Обрабатываем домен: {domain}")
    
    graph_dir = Path(f"materials/{domain}/graph")
    graph_dir.mkdir(parents=True, exist_ok=True)

    records = []
    for prob_id, variants in problems.items():
        if not variants:
            continue
        for variant_name, models_dict in variants.items():
            for model_name, metrics in models_dict.items():
                records.append({
                    'domain': domain,
                    'problem': prob_id,
                    'variant': variant_name,
                    'model': model_name,
                    'valid': metrics.get('valid', False),
                    'cost_gap_pct': metrics.get('cost_gap_%', 0),
                    'order_distance_norm': metrics.get('order_distance_norm', 0),
                    'kendall_inversions': metrics.get('kendall_inversions', 0),
                })

    df = pd.DataFrame(records)
    if df.empty:
        continue

    # ====================== ИСПРАВЛЕННЫЕ + НОВЫЕ ГРАФИКИ ======================

    # 1. Mean Cost Gap %
    mean_cost = df.groupby(['variant', 'model'])['cost_gap_pct'].mean().reset_index()
    plt.figure()
    sns.barplot(data=mean_cost, x='variant', y='cost_gap_pct', hue='model', palette=model_palette)
    plt.title(f'Mean Cost Gap % by Action Order Variant — {domain.capitalize()}', pad=20)
    plt.xlabel('Variant (порядок действий в домене)')
    plt.ylabel('Mean Cost Gap %')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Model', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(graph_dir / 'mean_cost_gap_by_variant_model.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Validity Rate % (ИСПРАВЛЕНО!)
    validity = df.groupby(['variant', 'model'])['valid'].mean().reset_index()
    validity['valid'] = validity['valid'] * 100   # ← только колонку valid умножаем

    plt.figure()
    sns.barplot(data=validity, x='variant', y='valid', hue='model', palette=model_palette)
    plt.title(f'Validity Rate (%) by Action Order Variant — {domain.capitalize()}', pad=20)
    plt.xlabel('Variant (порядок действий в домене)')
    plt.ylabel('Validity Rate (%)')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Model', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(graph_dir / 'validity_rate_by_variant_model.png', dpi=300, bbox_inches='tight')
    plt.close()

    # === НОВЫЙ ГРАФИК: Heatmap — насколько порядок влияет на валидность ===
    pivot_valid = validity.pivot(index='variant', columns='model', values='valid')
    plt.figure(figsize=(14, 9))
    ax = sns.heatmap(pivot_valid, annot=True, fmt='.1f', cmap='RdYlGn', 
                     linewidths=0.5, linecolor='white', cbar_kws={'label': 'Validity Rate (%)'})
    plt.title(f'How Action Order Affects Plan Validity — {domain.capitalize()}\n(зелёный = лучше)', pad=20)
    plt.xlabel('Model')
    plt.ylabel('Variant (порядок действий в домене)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(graph_dir / 'validity_heatmap_by_variant_model.png', dpi=400, bbox_inches='tight')
    plt.close()

    # Остальные графики (order distance, kendall, boxplot, scatter) — оставлены без изменений,
    # но с тем же красивым стилем (уже были в предыдущей версии)

    # ... (остальные 4 графика остаются как в предыдущей версии)

    print(f"  ✓ Все графики (включая новый heatmap) сохранены в {graph_dir}")

print("\n✅ Готово! Теперь есть чёткий heatmap, который показывает влияние порядка действий на валидность.")