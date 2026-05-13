from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from app.services.scheduler import compute_next_review


def get_or_create_daily_plan(db_path: Path, *, date: str, new_quota: int = 5) -> dict:
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT id, plan_date, new_quota, new_done, review_done FROM daily_plan WHERE plan_date = ?",
            (date,),
        ).fetchone()
        if row:
            return _plan_row_to_dict(row)

        conn.execute(
            """
            INSERT INTO daily_plan (plan_date, new_quota, new_done, review_done)
            VALUES (?, ?, 0, 0)
            """,
            (date, new_quota),
        )
        conn.commit()

        row = conn.execute(
            "SELECT id, plan_date, new_quota, new_done, review_done FROM daily_plan WHERE plan_date = ?",
            (date,),
        ).fetchone()
        return _plan_row_to_dict(row)


def seed_learning_state(db_path: Path, *, now: datetime) -> None:
    with sqlite3.connect(db_path) as conn:
        ids = conn.execute("SELECT id FROM amino_acids").fetchall()
        conn.executemany(
            """
            INSERT INTO learning_state
            (amino_id, status, last_seen_at, next_review_at, wrong_count, right_streak)
            VALUES (?, 'new', NULL, ?, 0, 0)
            """,
            [(row[0], now.isoformat()) for row in ids],
        )
        conn.commit()


def list_due_reviews(db_path: Path, *, now: datetime) -> list[dict]:
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT amino_id, wrong_count, next_review_at
            FROM learning_state
            WHERE next_review_at IS NOT NULL AND next_review_at <= ?
            """,
            (now.isoformat(),),
        ).fetchall()

    items = [
        {
            "amino_id": row[0],
            "wrong_count": row[1],
            "next_review_at": datetime.fromisoformat(row[2]),
        }
        for row in rows
    ]
    items.sort(key=lambda item: (-item["wrong_count"], item["next_review_at"]))
    return items


def list_new_items(db_path: Path, *, limit: int) -> list[dict]:
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT id, name_cn, name_en, abbr3, abbr1, image_path
            FROM amino_acids
            WHERE id NOT IN (SELECT amino_id FROM learning_state)
            ORDER BY id
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

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


def record_answer(
    db_path: Path,
    *,
    amino_id: int,
    is_correct: bool,
    now: datetime,
) -> None:
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            """
            SELECT wrong_count, right_streak
            FROM learning_state
            WHERE amino_id = ?
            """,
            (amino_id,),
        ).fetchone()
        if row is None:
            conn.execute(
                """
                INSERT INTO learning_state
                (amino_id, status, wrong_count, right_streak)
                VALUES (?, 'new', 0, 0)
                """,
                (amino_id,),
            )
            conn.commit()
            row = (0, 0)

        wrong_count, right_streak = row
        next_review_at, next_streak, next_wrong = compute_next_review(
            now=now,
            right_streak=right_streak,
            wrong_count=wrong_count,
            is_correct=is_correct,
        )

        conn.execute(
            """
            UPDATE learning_state
            SET last_seen_at = ?, next_review_at = ?, wrong_count = ?, right_streak = ?
            WHERE amino_id = ?
            """,
            (
                now.isoformat(),
                next_review_at.isoformat(),
                next_wrong,
                next_streak,
                amino_id,
            ),
        )
        conn.commit()


def _plan_row_to_dict(row: tuple) -> dict:
    return {
        "id": row[0],
        "plan_date": row[1],
        "new_quota": row[2],
        "new_done": row[3],
        "review_done": row[4],
    }
