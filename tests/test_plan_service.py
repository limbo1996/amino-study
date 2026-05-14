import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from app.db.learning_repo import seed_learning_state
from app.db.schema import init_db
from app.services.plan import build_today_plan


class TestPlanService(unittest.TestCase):
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

    def test_build_today_plan_prefers_due_reviews(self):
        now = datetime(2026, 5, 13, 9, 0, 0)
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "amino.db"
            init_db(db_path)
            self._seed_amino_acids(db_path, 3)
            seed_learning_state(db_path, now=now - timedelta(days=2))

            plan = build_today_plan(db_path, now=now)

            self.assertGreaterEqual(len(plan["reviews"]), 1)
            self.assertLessEqual(len(plan["new_items"]), 5)

    def test_build_today_plan_fills_new_items(self):
        now = datetime(2026, 5, 13, 9, 0, 0)
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "amino.db"
            init_db(db_path)
            self._seed_amino_acids(db_path, 6)

            plan = build_today_plan(db_path, now=now)

            self.assertEqual(len(plan["new_items"]), 5)


if __name__ == "__main__":
    unittest.main()
