from pathlib import Path
import shutil


def find_incomplete(domain: str = "folding"):
    """Показывает, какие проблемы/варианты ещё не готовы"""
    base = Path(f"materials/{domain}")
    incomplete = []

    for prob_dir in sorted(base.glob("p*")):
        prob_name = prob_dir.name
        for variant_dir in sorted(prob_dir.iterdir()):
            if not variant_dir.is_dir() or not (variant_dir / "domain.pddl").exists():
                continue
            variant_name = variant_dir.name

            models_ready = 0
            total_models = 0

            for model_dir in variant_dir.iterdir():
                if not model_dir.is_dir():
                    continue
                total_models += 1
                if (model_dir / "llm.plan").exists() and (model_dir / "llm_result.json").exists():
                    models_ready += 1
                else:
                    incomplete.append(f"{prob_name}/{variant_name}/{model_dir.name}")

            if models_ready < total_models:
                print(f"⚠️  {prob_name}/{variant_name} → {models_ready}/{total_models} моделей готово")

    if incomplete:
        print(f"\n🔴 Неполные комбинации ({len(incomplete)}):")
        for item in incomplete:
            print("   ", item)
    else:
        print("✅ Все комбинации завершены!")

if __name__ == "__main__":
    find_incomplete("folding")