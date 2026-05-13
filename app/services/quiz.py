from __future__ import annotations

import random


def generate_multiple_choice(
    items: list[dict],
    *,
    field: str,
    correct_index: int = 0,
) -> dict:
    if len(items) < 4:
        raise ValueError("At least 4 items required for multiple choice")

    correct_item = items[correct_index]
    correct_answer = correct_item[field]
    other_values = [item[field] for item in items if item[field] != correct_answer]
    if len(other_values) < 3:
        raise ValueError("Not enough unique options")

    options = random.sample(other_values, 3)
    options.append(correct_answer)
    random.shuffle(options)

    return {
        "field": field,
        "prompt": correct_item,
        "options": options,
        "answer": correct_answer,
    }


def generate_fill_in(item: dict, *, field: str) -> dict:
    return {
        "field": field,
        "prompt": item,
        "answer": item[field],
    }
