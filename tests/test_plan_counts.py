import sqlite3
import tempfile
import unittest
from pathlib import Path

from app.db.learning_repo import get_or_create_daily_plan, increment_plan_counts
from app.db.schema import init_db


class TestPlanCounts(unittest.TestCase):
    def test_increment_plan_counts_updates_totals(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "amino.db"
            init_db(db_path)

            plan = get_or_create_daily_plan(db_path, date="2026-05-13")
            increment_plan_counts(db_path, plan_id=plan["id"], new_done=1, review_done=2)

            with sqlite3.connect(db_path) as conn:
                row = conn.execute(
                    "SELECT new_done, review_done FROM daily_plan WHERE id = ?",
                    (plan["id"],),
                ).fetchone()

            self.assertEqual(row[0], 1)
            self.assertEqual(row[1], 2)


if __name__ == "__main__":
    unittest.main()
