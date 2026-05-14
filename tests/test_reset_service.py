import sqlite3
import tempfile
import unittest
from pathlib import Path

from app.db.schema import init_db
from app.services.reset import reset_progress


class TestResetService(unittest.TestCase):
    def test_reset_clears_progress(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "amino.db"
            init_db(db_path)

            with sqlite3.connect(db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO daily_plan (plan_date, new_quota, new_done, review_done)
                    VALUES ('2026-05-13', 5, 2, 1)
                    """
                )
                conn.execute(
                    """
                    INSERT INTO learning_state
                    (amino_id, status, wrong_count, right_streak)
                    VALUES (1, 'new', 1, 0)
                    """
                )
                conn.commit()

            reset_progress(db_path)

            with sqlite3.connect(db_path) as conn:
                plan_count = conn.execute("SELECT COUNT(*) FROM daily_plan").fetchone()[0]
                state_count = conn.execute("SELECT COUNT(*) FROM learning_state").fetchone()[0]

            self.assertEqual(plan_count, 0)
            self.assertEqual(state_count, 0)


if __name__ == "__main__":
    unittest.main()
