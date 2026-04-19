import json
import random
import re
from pathlib import Path
from typing import Any


def get_action_name(action_block: str) -> str | None:
    match = re.search(r"\(\s*:action\s+([^\s)]+)", action_block, re.IGNORECASE)
    return match.group(1) if match else None


def extract_actions_blocks(domain_text: str) -> tuple[str, dict[str, str], str, list[str]]:
    action_map: dict[str, str] = {}
    canonical_order_list: list[str] = []
    index = 0
    text_length = len(domain_text)

    while index < text_length:
        if domain_text[index] == ";":
            while index < text_length and domain_text[index] != "\n":
                index += 1
            if index < text_length:
                index += 1
            continue

        if index + 8 <= text_length and domain_text[index:index + 8].lower() == "(:action":
            start = index
            while start > 0 and domain_text[start - 1] in " \t\n":
                start -= 1

            depth = 0
            cursor = index
            while cursor < text_length:
                if domain_text[cursor] == "(":
                    depth += 1
                elif domain_text[cursor] == ")":
                    depth -= 1
                    if depth == 0:
                        block = domain_text[start:cursor + 1]
                        name = get_action_name(block)
                        if name:
                            action_map[name] = block
                            canonical_order_list.append(name)
                        index = cursor + 1
                        break
                cursor += 1
            continue
        index += 1

    if not action_map:
        return domain_text, {}, "", []

    first_block = next(iter(action_map.values()))
    first_pos = domain_text.find(first_block)
    header = domain_text[:first_pos].rstrip()

    last_block = list(action_map.values())[-1]
    last_pos = domain_text.rfind(last_block) + len(last_block)
    footer = domain_text[last_pos:].lstrip("\n")

    return header, action_map, footer, canonical_order_list


def get_plan_order(plan_text: str, canonical_order_list: list[str]) -> list[str]:
    action_names = re.findall(r"\(([\w-]+)", plan_text)
    seen: set[str] = set()
    plan_order: list[str] = []
    for name in action_names:
        if name in canonical_order_list and name not in seen:
            seen.add(name)
            plan_order.append(name)
    for action in canonical_order_list:
        if action not in seen:
            plan_order.append(action)
    return plan_order


def get_frequency_order(plan_text: str, canonical_order_list: list[str]) -> list[str]:
    action_names = re.findall(r"\(([\w-]+)", plan_text)
    counts = {action: 0 for action in canonical_order_list}
    for name in action_names:
        if name in counts:
            counts[name] += 1
    return sorted(counts, key=counts.get, reverse=True)


def kendall_tau_dist(order1: list[str], order2: list[str]) -> int:
    positions = {action: idx for idx, action in enumerate(order2)}
    inversions = 0
    for idx in range(len(order1)):
        for jdx in range(idx + 1, len(order1)):
            if positions[order1[idx]] > positions[order1[jdx]]:
                inversions += 1
    return inversions


def get_dispersion_order_with_source(random_orders_list: list[list[str]], freq_order: list[str]) -> tuple[list[str], int]:
    max_dist = -1
    best_order: list[str] | None = None
    best_idx = -1
    for idx, candidate in enumerate(random_orders_list):
        distance = kendall_tau_dist(candidate, freq_order)
        if distance > max_dist:
            max_dist = distance
            best_order = candidate[:]
            best_idx = idx
    return (best_order or []), best_idx


def shuffle(
    domain_path: str | Path,
    problem_path: str | Path,
    optimal_plan_path: str | Path,
    save_dir: str | Path,
    seed: int = 52,
    problem_id: str | None = None,
    sampling_profile: list[str] | None = None,
    variant_generation_version: str = "v2",
) -> None:
    domain_path = Path(domain_path)
    problem_path = Path(problem_path)
    optimal_plan_path = Path(optimal_plan_path)
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    rng = random.Random(seed)

    domain_text = domain_path.read_text(encoding="utf-8")
    header, action_map, footer, canonical_order_list = extract_actions_blocks(domain_text)

    random_order_list: list[list[str]] = []
    for _ in range(10):
        shuffled = canonical_order_list[:]
        rng.shuffle(shuffled)
        random_order_list.append(shuffled)

    optimal_plan_text = optimal_plan_path.read_text(encoding="utf-8")
    optimal_order_list = get_plan_order(optimal_plan_text, canonical_order_list)
    frequency_order_list = get_frequency_order(optimal_plan_text, canonical_order_list)
    dispersion_order_list, chosen_idx = get_dispersion_order_with_source(random_order_list, frequency_order_list)

    def save_domain(subdir_name: str, order_list: list[str]) -> None:
        subdir = save_dir / subdir_name
        subdir.mkdir(parents=True, exist_ok=True)
        path = subdir / "domain.pddl"
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(header + "\n")
            for action in order_list:
                handle.write(action_map[action])
            handle.write(footer)

    save_domain("canonical", canonical_order_list)
    save_domain("optimal", optimal_order_list)
    save_domain("frequency", frequency_order_list)
    save_domain("dispersion", dispersion_order_list)

    selected_random = rng.sample(random_order_list, 5)
    for idx, order in enumerate(selected_random, start=1):
        save_domain(f"random_{idx:02d}", order)

    print(f"Generated {save_dir.name}: 4 curated variants + 5 random variants")

    meta: dict[str, Any] = {
        "seed": seed,
        "problem_id": problem_id or problem_path.stem,
        "sampling_profile": sampling_profile or [],
        "variant_generation_version": variant_generation_version,
        "canonical": canonical_order_list,
        "optimal": optimal_order_list,
        "frequency": frequency_order_list,
        "dispersion": dispersion_order_list,
        "dispersion_from_random_idx": chosen_idx + 1 if chosen_idx >= 0 else None,
        "all_random_orders": random_order_list,
        "selected_random_orders": selected_random,
    }
    with open(save_dir / "shuffle_meta.json", "w", encoding="utf-8") as handle:
        json.dump(meta, handle, ensure_ascii=False, indent=2)
