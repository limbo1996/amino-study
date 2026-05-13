from __future__ import annotations

from datetime import datetime, timedelta
from typing import Iterable

REVIEW_INTERVALS_DAYS = (1, 2, 4, 7, 15)


def compute_next_review(
    *,
    now: datetime,
    right_streak: int,
    wrong_count: int,
    is_correct: bool,
) -> tuple[datetime, int, int]:
    if not is_correct:
        return now + timedelta(days=REVIEW_INTERVALS_DAYS[0]), 0, wrong_count + 1

    next_streak = right_streak + 1
    interval_index = min(next_streak - 1, len(REVIEW_INTERVALS_DAYS) - 1)
    interval_days = REVIEW_INTERVALS_DAYS[interval_index]
    return now + timedelta(days=interval_days), next_streak, wrong_count


def prioritize_due_reviews(
    items: Iterable[dict],
    *,
    now: datetime,
) -> list[dict]:
    due_items = [item for item in items if item["next_review_at"] <= now]
    return sorted(
        due_items,
        key=lambda item: (-item["wrong_count"], item["next_review_at"]),
    )
