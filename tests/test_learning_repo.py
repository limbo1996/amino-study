import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from app.db.learning_repo import (
    get_or_create_daily_plan,
    list_due_reviews,
    list_new_items,
    record_answer,
    seed_learning_state,
)
from app.db.schema import init_db


class TestLearningRepo(unittest.TestCase):
    def _seed_amino_acids(self, db_path: Path, count: int) -> None:
        with sqlite3.connect(db_path) as conn:
            for i in range(count):
                conn.execute(
                    """
                    INSERT INTO amino_acids
                    (name_cn, name_en, abbr3, abbr1, image_path, formula)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        f"中文{i}",
                        f"EN{i}",
                        f"A{i}",
                        f"X{i}",
                        f"/tmp/{i}.png",
                        "",
                    ),
                )
            conn.commit()

    def test_daily_plan_defaults_to_five(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "amino.db"
            init_db(db_path)

            plan = get_or_create_daily_plan(db_path, date="2026-05-13")

            self.assertEqual(plan["new_quota"], 5)

    def test_due_reviews_prioritize_wrong_count(self):
        now = datetime(2026, 5, 13, 9, 0, 0)
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "amino.db"
            init_db(db_path)
            self._seed_amino_acids(db_path, 2)

            seed_learning_state(db_path, now=now - timedelta(days=2))
            with sqlite3.connect(db_path) as conn:
                conn.execute(
                    "UPDATE learning_state SET wrong_count = 1 WHERE amino_id = 1"
                )
                conn.execute(
                    "UPDATE learning_state SET wrong_count = 3 WHERE amino_id = 2"
                )
                conn.commit()

            due = list_due_reviews(db_path, now=now)
            due_ids = [item["amino_id"] for item in due]

            self.assertEqual(due_ids, [2, 1])

    def test_record_answer_updates_review_state(self):
        now = datetime(2026, 5, 13, 9, 0, 0)
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "amino.db"
            init_db(db_path)
            self._seed_amino_acids(db_path, 1)

            seed_learning_state(db_path, now=now - timedelta(days=2))
            record_answer(db_path, amino_id=1, is_correct=False, now=now)

            with sqlite3.connect(db_path) as conn:
                row = conn.execute(
                    """
                    SELECT wrong_count, right_streak, next_review_at
                    FROM learning_state
                    WHERE amino_id = 1
                    """
                ).fetchone()

            self.assertEqual(row[0], 1)
            self.assertEqual(row[1], 0)
            self.assertIsNotNone(row[2])

    def test_list_new_items_excludes_existing_learning_state(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "amino.db"
            init_db(db_path)
            self._seed_amino_acids(db_path, 3)

            with sqlite3.connect(db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO learning_state
                    (amino_id, status, wrong_count, right_streak)
                    VALUES (1, 'new', 0, 0)
                    """
                )
                conn.commit()

            items = list_new_items(db_path, limit=2)
            ids = [item["id"] for item in items]

            self.assertEqual(ids, [2, 3])


if __name__ == "__main__":
    unittest.main()
