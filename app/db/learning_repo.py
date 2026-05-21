from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from app.services.scheduler import compute_next_review


def get_daily_streak(db_path: Path, *, amino_id: int, today: str) -> int:
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT daily_streak, daily_streak_date FROM learning_state WHERE amino_id = ?",
            (amino_id,),
        ).fetchone()
        if row is None:
            return 0
        streak, streak_date = row
        if streak_date != today:
            conn.execute(
                "UPDATE learning_state SET daily_streak = 0, daily_streak_date = ? WHERE amino_id = ?",
                (today, amino_id),
            )
            conn.commit()
            return 0
        return min(streak, 5)


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


def increment_plan_counts(
    db_path: Path,
    *,
    plan_id: int,
    new_done: int = 0,
    review_done: int = 0,
) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            UPDATE daily_plan
            SET new_done = new_done + ?, review_done = review_done + ?
            WHERE id = ?
            """,
            (new_done, review_done, plan_id),
        )
        conn.commit()


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
        sql = """
            SELECT id, name_cn, name_en, abbr3, abbr1, image_path
            FROM amino_acids
            WHERE id NOT IN (SELECT amino_id FROM learning_state)
            ORDER BY id
        """
        if limit >= 0:
            sql += " LIMIT ?"
            rows = conn.execute(sql, (limit,)).fetchall()
        else:
            rows = conn.execute(sql).fetchall()

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
    today = now.date().isoformat()
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            """
            SELECT wrong_count, right_streak, daily_streak, daily_streak_date
            FROM learning_state
            WHERE amino_id = ?
            """,
            (amino_id,),
        ).fetchone()
        if row is None:
            conn.execute(
                """
                INSERT INTO learning_state
                (amino_id, status, wrong_count, right_streak, daily_streak, daily_streak_date)
                VALUES (?, 'new', 0, 0, 0, ?)
                """,
                (amino_id, today),
            )
            conn.commit()
            row = (0, 0, 0, today)

        wrong_count, right_streak, daily_streak, streak_date = row
        if streak_date != today:
            daily_streak = 0

        if is_correct:
            daily_streak += 1
            if daily_streak >= 5:
                next_review_at, next_streak, next_wrong = compute_next_review(
                    now=now,
                    right_streak=right_streak,
                    wrong_count=wrong_count,
                    is_correct=True,
                )
                conn.execute(
                    """
                    UPDATE learning_state
                    SET last_seen_at = ?, next_review_at = ?, wrong_count = ?, right_streak = ?,
                        daily_streak = 5, daily_streak_date = ?
                    WHERE amino_id = ?
                    """,
                    (now.isoformat(), next_review_at.isoformat(), next_wrong, next_streak, today, amino_id),
                )
                conn.commit()
                conn.execute(
                    "UPDATE daily_plan SET new_done = new_done + 1 WHERE plan_date = ?",
                    (today,),
                )
                conn.commit()
            else:
                conn.execute(
                    """
                    UPDATE learning_state
                    SET daily_streak = ?, daily_streak_date = ?
                    WHERE amino_id = ?
                    """,
                    (daily_streak, today, amino_id),
                )
                conn.commit()
        else:
            conn.execute(
                """
                UPDATE learning_state
                SET wrong_count = wrong_count + 1, right_streak = 0,
                    daily_streak = 0, daily_streak_date = ?
                WHERE amino_id = ?
                """,
                (today, amino_id),
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
