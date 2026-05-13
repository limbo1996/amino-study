from __future__ import annotations

from datetime import datetime
from pathlib import Path

from app.db.learning_repo import record_answer
from app.services.plan import build_today_plan
from app.services.quiz import generate_fill_in, generate_multiple_choice


def build_session(db_path: Path, *, now: datetime) -> dict:
    plan_bundle = build_today_plan(db_path, now=now)
    questions = []

    for review in plan_bundle["reviews"]:
        question = {
            "type": "review",
            "amino_id": review["amino_id"],
            "field": "name_en",
            "answer": None,
        }
        questions.append(question)

    for item in plan_bundle["new_items"]:
        fill_in = generate_fill_in(item, field="abbr1")
        questions.append(
            {
                "type": "new",
                "amino_id": item["id"],
                "field": "abbr1",
                "answer": fill_in["answer"],
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
    amino_id: int,
    is_correct: bool,
    now: datetime,
) -> None:
    record_answer(db_path, amino_id=amino_id, is_correct=is_correct, now=now)


def generate_review_question(
    items: list[dict],
    *,
    correct_index: int = 0,
) -> dict:
    return generate_multiple_choice(items, field="name_en", correct_index=correct_index)
