from __future__ import annotations

import random


def generate_abbr_question(
    items: list[dict],
    *,
    correct_index: int = 0,
    format_type: str | None = None,
) -> dict:
    if len(items) < 4:
        raise ValueError("At least 4 items required for multiple choice")

    if format_type is None:
        format_type = random.choice(["abbr1", "abbr3"])
    if format_type not in {"abbr1", "abbr3"}:
        raise ValueError("Invalid format type")

    correct_item = items[correct_index]
    correct_answer = correct_item[format_type]
    other_values = [item[format_type] for item in items if item[format_type] != correct_answer]
    if len(other_values) < 3:
        raise ValueError("Not enough unique options")

    options = random.sample(other_values, 3)
    options.append(correct_answer)
    random.shuffle(options)

    return {
        "format": format_type,
        "options": options,
        "answer": correct_answer,
        "prompt": correct_item,
    }
