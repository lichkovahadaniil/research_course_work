import json
import re
from pathlib import Path


VARIANT_NAMES = [
    "frequency",
    "dispersion_01",
    "dispersion_02",
    "dispersion_03",
    "dispersion_04",
    "dispersion_05",
]

ACTION_PATTERN = re.compile(r"\(\s*:action\s+([^\s)]+)", re.IGNORECASE)
PLAN_ACTION_PATTERN = re.compile(r"^\s*\(([\w-]+)", re.MULTILINE)


def _extract_action_blocks(domain_text: str) -> tuple[str, dict[str, str], str, list[str]]:
    action_blocks: dict[str, str] = {}
    action_order: list[str] = []
    cursor = 0
    text_length = len(domain_text)

    while cursor < text_length:
        start = domain_text.lower().find("(:action", cursor)
        if start == -1:
            break

        block_start = start
        while block_start > 0 and domain_text[block_start - 1] in " \t\n":
            block_start -= 1

        depth = 0
        block_end = start
        while block_end < text_length:
            if domain_text[block_end] == "(":
                depth += 1
            elif domain_text[block_end] == ")":
                depth -= 1
                if depth == 0:
                    block_end += 1
                    break
            block_end += 1

        block = domain_text[block_start:block_end]
        match = ACTION_PATTERN.search(block)
        if match:
            action_name = match.group(1)
            action_blocks[action_name] = block
            action_order.append(action_name)

        cursor = block_end

    if not action_order:
        return domain_text, {}, "", []

    first_block = action_blocks[action_order[0]]
    last_block = action_blocks[action_order[-1]]
    header = domain_text[:domain_text.find(first_block)].rstrip()
    footer_start = domain_text.rfind(last_block) + len(last_block)
    footer = domain_text[footer_start:].lstrip("\n")
    return header, action_blocks, footer, action_order


def _extract_frequency_order(plan_text: str, action_order: list[str]) -> list[str]:
    counts = {action: 0 for action in action_order}
    for action_name in PLAN_ACTION_PATTERN.findall(plan_text):
        if action_name in counts:
            counts[action_name] += 1

    original_positions = {action: index for index, action in enumerate(action_order)}
    return sorted(
        action_order,
        key=lambda action: (-counts[action], original_positions[action]),
    )


def _rotate_right(items: list[str], steps: int) -> list[str]:
    if not items:
        return []
    offset = steps % len(items)
    if offset == 0:
        return items[:]
    return items[-offset:] + items[:-offset]


def _write_domain_variant(
    header: str,
    action_blocks: dict[str, str],
    footer: str,
    action_order: list[str],
    variant_dir: Path,
) -> None:
    variant_dir.mkdir(parents=True, exist_ok=True)
    domain_path = variant_dir / "domain.pddl"
    content = [header, "\n"]
    for action_name in action_order:
        content.append(action_blocks[action_name])
    content.append(footer)
    domain_path.write_text("".join(content), encoding="utf-8")


def shuffle(
    domain_path: str | Path,
    problem_path: str | Path,
    optimal_plan_path: str | Path,
    save_dir: str | Path,
    seed: int = 52,
    problem_id: str | None = None,
) -> None:
    domain_path = Path(domain_path)
    problem_path = Path(problem_path)
    optimal_plan_path = Path(optimal_plan_path)
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    domain_text = domain_path.read_text(encoding="utf-8")
    plan_text = optimal_plan_path.read_text(encoding="utf-8")
    header, action_blocks, footer, action_order = _extract_action_blocks(domain_text)
    frequency_order = _extract_frequency_order(plan_text, action_order)

    variants = {
        "frequency": frequency_order,
        **{
            f"dispersion_{index:02d}": _rotate_right(frequency_order, index)
            for index in range(1, 6)
        },
    }

    for variant_name, variant_order in variants.items():
        _write_domain_variant(header, action_blocks, footer, variant_order, save_dir / variant_name)

    metadata = {
        "seed": seed,
        "problem_id": problem_id or problem_path.stem,
        "variants": list(variants),
    }
    (save_dir / "shuffle_meta.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
