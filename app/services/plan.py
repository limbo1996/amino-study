from __future__ import annotations

from datetime import datetime
from pathlib import Path

from app.db.learning_repo import get_or_create_daily_plan, list_due_reviews, list_new_items


def build_today_plan(db_path: Path, *, now: datetime) -> dict:
    plan = get_or_create_daily_plan(db_path, date=now.date().isoformat())
    reviews = list_due_reviews(db_path, now=now)
    new_items = list_new_items(db_path, limit=-1)

    return {
        "plan": plan,
        "reviews": reviews,
        "new_items": new_items,
    }
