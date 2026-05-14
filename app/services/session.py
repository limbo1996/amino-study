from __future__ import annotations

from datetime import datetime
from pathlib import Path

from app.db.learning_repo import increment_plan_counts, record_answer
from app.services.plan import build_today_plan
from app.services.quiz import generate_fill_in, generate_multiple_choice


def build_session(db_path: Path, *, now: datetime, rng_seed: int | None = None) -> dict:
    plan_bundle = build_today_plan(db_path, now=now)
    questions = []

    if rng_seed is not None:
        import random

        random.seed(rng_seed)

    if plan_bundle["reviews"]:
        review_ids = [review["amino_id"] for review in plan_bundle["reviews"]]
        review_items = _fetch_items_by_ids(db_path, review_ids)
        if len(review_items) >= 4:
            question = generate_review_question(review_items)
            questions.append(
                {
                    "type": "review",
                    "amino_id": question["prompt"]["id"],
                    "field": question["field"],
                    "options": question["options"],
                    "answer": question["answer"],
                    "image_path": question["prompt"]["image_path"],
                }
            )

    for item in plan_bundle["new_items"]:
        fill_in = generate_fill_in(item, field="abbr1")
        questions.append(
            {
                "type": "new",
                "amino_id": item["id"],
                "field": "abbr1",
                "answer": fill_in["answer"],
                "image_path": item["image_path"],
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
    if question_type == "new":
        increment_plan_counts(db_path, plan_id=plan_id, new_done=1)
    elif question_type == "review":
        increment_plan_counts(db_path, plan_id=plan_id, review_done=1)


def generate_review_question(
    items: list[dict],
    *,
    correct_index: int = 0,
) -> dict:
    return generate_multiple_choice(items, field="name_en", correct_index=correct_index)


def _fetch_items_by_ids(db_path: Path, ids: list[int]) -> list[dict]:
    if not ids:
        return []

    import sqlite3

    placeholders = ",".join("?" for _ in ids)
    query = (
        "SELECT id, name_cn, name_en, abbr3, abbr1, image_path "
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
        }
        for row in rows
    ]
