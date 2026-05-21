from __future__ import annotations

from datetime import datetime
import random
from pathlib import Path

from app.db.learning_repo import get_daily_streak, record_answer
from app.services.plan import build_today_plan
from app.services.quiz import generate_abbr_question


def build_session(db_path: Path, *, now: datetime, rng_seed: int | None = None) -> dict:
    today = now.date().isoformat()
    plan_bundle = build_today_plan(db_path, now=now)
    plan = plan_bundle["plan"]

    review_ids = [review["amino_id"] for review in plan_bundle["reviews"]]
    new_item_ids = [item["id"] for item in plan_bundle["new_items"]]

    review_active = [
        rid for rid in review_ids
        if get_daily_streak(db_path, amino_id=rid, today=today) < 5
    ]

    new_slots = max(plan["new_quota"] - plan["new_done"], 0)
    new_active = [
        nid for nid in new_item_ids
        if get_daily_streak(db_path, amino_id=nid, today=today) < 5
    ][:new_slots]

    active_ids = review_active + new_active

    questions = []
    candidates = _fetch_items_by_ids(db_path, active_ids)

    if len(candidates) >= 4:
        for candidate in candidates:
            question = generate_abbr_question(
                candidates,
                correct_index=candidates.index(candidate),
                format_type=None,
            )
            questions.append(
                {
                    "type": "choice",
                    "amino_id": candidate["id"],
                    "daily_streak": get_daily_streak(db_path, amino_id=candidate["id"], today=today),
                    "format": question["format"],
                    "options": question["options"],
                    "answer": question["answer"],
                    "image_path": candidate["image_path"],
                    "name_cn": candidate["name_cn"],
                    "name_en": candidate["name_en"],
                    "formula": candidate["formula"],
                }
            )

    return {
        "plan": plan_bundle["plan"],
        "reviews": plan_bundle["reviews"],
        "new_items": plan_bundle["new_items"],
        "questions": questions,
    }


def record_session_answer(
    db_path: Path,
    *,
    plan_id: int,
    question_type: str,
    amino_id: int,
    is_correct: bool,
    now: datetime,
) -> None:
    record_answer(db_path, amino_id=amino_id, is_correct=is_correct, now=now)


def _fetch_items_by_ids(db_path: Path, ids: list[int]) -> list[dict]:
    if not ids:
        return []

    import sqlite3

    placeholders = ",".join("?" for _ in ids)
    query = (
        "SELECT id, name_cn, name_en, abbr3, abbr1, image_path, formula "
        f"FROM amino_acids WHERE id IN ({placeholders})"
    )
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(query, ids).fetchall()

    return [
        {
            "id": row[0],
            "name_cn": row[1],
            "name_en": row[2],
            "abbr3": row[3],
            "abbr1": row[4],
            "image_path": row[5],
            "formula": row[6],
        }
        for row in rows
    ]
