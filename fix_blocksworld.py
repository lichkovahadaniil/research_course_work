from pathlib import Path
import re

instances_dir = Path("domains/original/blocksworld/instances")

print(f"Исправляем файлы в: {instances_dir}\n")

for pddl_file in sorted(instances_dir.glob("instance-*.pddl")):
    original_text = pddl_file.read_text(encoding="utf-8")
    text = original_text

    # Основные замены
    text = re.sub(r'\(:INIT', '(:init', text, flags=re.IGNORECASE)
    text = re.sub(r'\(:GOAL', '(:goal', text, flags=re.IGNORECASE)
    text = re.sub(r'\bAND\b', 'and', text, flags=re.IGNORECASE)

    # Убираем возможный мусор в конце файла
    text = text.replace('%', '').strip()

    # Дополнительно: делаем :goal более читаемым (опционально, но полезно)
    text = re.sub(r'\(:goal\s*\(and', '(:goal (and', text)

    if text != original_text:
        pddl_file.write_text(text, encoding="utf-8")
        print(f"✓ Исправлен: {pddl_file.name}")
    else:
        print(f"○ Уже норм: {pddl_file.name}")

print("\n✅ Все файлы обработаны!")