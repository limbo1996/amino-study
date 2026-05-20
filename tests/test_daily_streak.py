import unittest
from datetime import datetime, timedelta
from pathlib import Path

from app.db.learning_repo import (
    get_or_create_daily_plan,
    record_answer,
    seed_learning_state,
    get_daily_streak,
)
from app.db.schema import init_db, migrate_add_daily_streak


class TestDailyStreak(unittest.TestCase):
    def _setup_db(self, db_path: Path):
        import sqlite3

        from app.db.schema import init_db, migrate_add_daily_streak

        init_db(db_path)
        migrate_add_daily_streak(db_path)
        with sqlite3.connect(db_path) as conn:
            for i in range(8):
                conn.execute(
                    "INSERT INTO amino_acids (name_cn, name_en, abbr3, abbr1, image_path, formula) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (f"中文{i}", f"EN{i}", f"A{i}", f"X{i}", f"/tmp/{i}.png", ""),
                )
            conn.commit()
        seed_learning_state(db_path, now=datetime(2026, 5, 13, 9, 0, 0))

    def test_daily_streak_starts_at_zero(self):
        with __import__("tempfile").TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "amino.db"
            self._setup_db(db_path)

            streak = get_daily_streak(db_path, amino_id=1, today="2026-05-13")
            self.assertEqual(streak, 0)

    def test_correct_increments_daily_streak(self):
        with __import__("tempfile").TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "amino.db"
            self._setup_db(db_path)
            now = datetime(2026, 5, 13, 9, 0, 0)

            for expected in [1, 2, 3, 4, 5]:
                record_answer(db_path, amino_id=1, is_correct=True, now=now)
                streak = get_daily_streak(db_path, amino_id=1, today="2026-05-13")
                self.assertEqual(streak, expected, f"Expected {expected} after {expected} correct answers")

            record_answer(db_path, amino_id=1, is_correct=True, now=now)
            streak = get_daily_streak(db_path, amino_id=1, today="2026-05-13")
            self.assertEqual(streak, 5, "streak stays at 5 after completion")

    def test_wrong_resets_daily_streak_to_zero(self):
        with __import__("tempfile").TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "amino.db"
            self._setup_db(db_path)
            now = datetime(2026, 5, 13, 9, 0, 0)

            record_answer(db_path, amino_id=1, is_correct=True, now=now)
            record_answer(db_path, amino_id=1, is_correct=True, now=now)
            record_answer(db_path, amino_id=1, is_correct=False, now=now)

            streak = get_daily_streak(db_path, amino_id=1, today="2026-05-13")
            self.assertEqual(streak, 0)

    def test_plan_increments_only_on_streak_five(self):
        with __import__("tempfile").TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "amino.db"
            self._setup_db(db_path)
            now = datetime(2026, 5, 13, 9, 0, 0)

            plan = get_or_create_daily_plan(db_path, date="2026-05-13")
            self.assertEqual(plan["new_done"], 0)

            record_answer(db_path, amino_id=1, is_correct=True, now=now)
            plan = get_or_create_daily_plan(db_path, date="2026-05-13")
            self.assertEqual(plan["new_done"], 0, "new_done should not increment before streak 5")

            for _ in range(4):
                record_answer(db_path, amino_id=1, is_correct=True, now=now)

            plan = get_or_create_daily_plan(db_path, date="2026-05-13")
            self.assertEqual(plan["new_done"], 1, "new_done should increment at streak 5")

    def test_wrong_resets_review_streak(self):
        with __import__("tempfile").TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "amino.db"
            self._setup_db(db_path)
            now = datetime(2026, 5, 13, 9, 0, 0)

            for _ in range(5):
                record_answer(db_path, amino_id=1, is_correct=True, now=now)

            import sqlite3
            with sqlite3.connect(db_path) as conn:
                row = conn.execute(
                    "SELECT right_streak FROM learning_state WHERE amino_id=1"
                ).fetchone()
            self.assertEqual(row[0], 1, "right_streak should be 1 after 5 correct")

            record_answer(db_path, amino_id=1, is_correct=False, now=now)

            with sqlite3.connect(db_path) as conn:
                row = conn.execute(
                    "SELECT right_streak, daily_streak FROM learning_state WHERE amino_id=1"
                ).fetchone()
            self.assertEqual(row[0], 0, "right_streak should reset to 0 on wrong")
            self.assertEqual(row[1], 0, "daily_streak should reset to 0 on wrong")


if __name__ == "__main__":
    unittest.main()
