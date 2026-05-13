import unittest
from pathlib import Path

from app.data.loader import load_amino_acids


class TestDataLoader(unittest.TestCase):
    def test_loads_twenty_amino_acids(self):
        repo_root = Path(__file__).resolve().parents[1]
        csv_path = repo_root / "deepseek_csv_20260513_f1933c.csv"

        records = load_amino_acids(csv_path)

        self.assertEqual(len(records), 20)
        self.assertIn("name_cn", records[0])
        self.assertIn("abbr1", records[0])


if __name__ == "__main__":
    unittest.main()
