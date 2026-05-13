import sqlite3
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from app.db.schema import init_db
from app.services.session import build_session, record_session_answer


class TestSessionService(unittest.TestCase):
    def _seed_amino_acids(self, db_path: Path, count: int) -> None:
        with sqlite3.connect(db_path) as conn:
            for i in range(count):
                conn.execute(
                    """
                    INSERT INTO amino_acids
                    (name_cn, name_en, abbr3, abbr1, image_path)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        f"中文{i}",
                        f"EN{i}",
                        f"A{i}",
                        f"X{i}",
                        f"/tmp/{i}.png",
                    ),
                )
            conn.commit()

    def test_build_session_returns_questions(self):
        now = datetime(2026, 5, 13, 9, 0, 0)
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "amino.db"
            init_db(db_path)
            self._seed_amino_acids(db_path, 6)

            session = build_session(db_path, now=now)

            self.assertGreaterEqual(len(session["questions"]), 1)
            self.assertIn("plan", session)

    def test_record_session_answer_updates_state(self):
        now = datetime(2026, 5, 13, 9, 0, 0)
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "amino.db"
            init_db(db_path)
            self._seed_amino_acids(db_path, 1)

            session = build_session(db_path, now=now)
            question = session["questions"][0]

            record_session_answer(
                db_path,
                amino_id=question["amino_id"],
                is_correct=False,
                now=now,
            )

            with sqlite3.connect(db_path) as conn:
                row = conn.execute(
                    """
                    SELECT wrong_count, right_streak
                    FROM learning_state
                    WHERE amino_id = ?
                    """,
                    (question["amino_id"],),
                ).fetchone()

            self.assertEqual(row[0], 1)
            self.assertEqual(row[1], 0)


if __name__ == "__main__":
    unittest.main()
