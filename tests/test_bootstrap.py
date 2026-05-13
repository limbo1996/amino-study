import sqlite3
import tempfile
import unittest
from pathlib import Path

from app.bootstrap import bootstrap_storage


class TestBootstrap(unittest.TestCase):
    def test_bootstrap_seeds_database(self):
        repo_root = Path(__file__).resolve().parents[1]
        csv_path = repo_root / "deepseek_csv_20260513_f1933c.csv"

        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "amino.db"

            bootstrap_storage(db_path, csv_path)

            with sqlite3.connect(db_path) as conn:
                count = conn.execute("SELECT COUNT(*) FROM amino_acids").fetchone()[0]

            self.assertEqual(count, 20)


if __name__ == "__main__":
    unittest.main()
