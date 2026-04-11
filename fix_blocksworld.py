from pathlib import Path

DOMAIN_TYPES = ['folding', 'labyrinth', 'recharging-robots', 'ricochet-robots', 'rubiks-cube']

def cleanup_random_dispersion_source(dry_run: bool = True):
    """
    Удаляет все старые domain_random_dispersion_source.pddl
    dry_run=True — только покажет, что будет удалено (рекомендую сначала так)
    """
    deleted = 0
    for domain in DOMAIN_TYPES:
        base_path = Path(f'materials/{domain}')
        for i in range(1, 21):
            folder = base_path / f'p{i:02d}'
            target = folder / 'domain_random_dispersion_source.pddl'
            
            if target.exists():
                if dry_run:
                    print(f"[DRY-RUN] Будет удалён → {target}")
                else:
                    target.unlink()
                    print(f"🗑 Удалён → {target}")
                deleted += 1
    
    print(f"\n{'='*60}")
    print(f"✅ Завершено! Найдено и {'удалено' if not dry_run else 'готово к удалению'}: {deleted} файлов")
    if dry_run:
        print("   Запусти с dry_run=False чтобы реально удалить файлы.")

# ====================== ЗАПУСК ======================

if __name__ == "__main__":
    # Сначала безопасный режим (покажет, что будет удалено)
    cleanup_random_dispersion_source(dry_run=False)
    
    # После того как убедишься, что всё правильно — раскомментируй строку ниже:
    # cleanup_random_dispersion_source(dry_run=False)