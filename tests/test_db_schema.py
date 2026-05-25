import sqlite3
import tempfile
import unittest
from pathlib import Path

from app.db.schema import init_db, migrate_add_nature


class TestDbSchema(unittest.TestCase):
    def test_migrate_add_nature_creates_column(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "amino.db"
            init_db(db_path)

            migrate_add_nature(db_path)

            with sqlite3.connect(db_path) as conn:
                rows = conn.execute("PRAGMA table_info(amino_acids)").fetchall()
            columns = [row[1] for row in rows]
            self.assertIn("nature", columns)

    def test_migrate_add_nature_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "amino.db"
            init_db(db_path)

            migrate_add_nature(db_path)
            migrate_add_nature(db_path)

            with sqlite3.connect(db_path) as conn:
                rows = conn.execute("PRAGMA table_info(amino_acids)").fetchall()
            columns = [row[1] for row in rows]
            nature_cols = [c for c in columns if c == "nature"]
            self.assertEqual(len(nature_cols), 1)


if __name__ == "__main__":
    unittest.main()
