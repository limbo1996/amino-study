import sqlite3
import tempfile
import unittest
from pathlib import Path

from app.db.schema import init_db
from app.services.seed import ensure_seeded


class TestDbSeed(unittest.TestCase):
    def test_seed_inserts_records_when_empty(self):
        repo_root = Path(__file__).resolve().parents[1]
        csv_path = repo_root / "deepseek_csv_20260513_f1933c.csv"

        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "amino.db"

            init_db(db_path)
            ensure_seeded(db_path, csv_path)

            with sqlite3.connect(db_path) as conn:
                count = conn.execute("SELECT COUNT(*) FROM amino_acids").fetchone()[0]

            self.assertEqual(count, 20)


if __name__ == "__main__":
    unittest.main()
