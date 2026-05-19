import tempfile
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

    def test_normalizes_image_paths_to_fig_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            csv_path = temp_path / "data.csv"
            csv_path.write_text(
                "中文名,英文名,三字缩写,单字缩写,图片路径\n"
                "丙氨酸,Alanine,Ala,A,fig/A.png\n",
                encoding="utf-8",
            )

            records = load_amino_acids(csv_path, repo_root=temp_path)

            self.assertEqual(records[0]["image_path"], str(temp_path / "fig" / "A.png"))


if __name__ == "__main__":
    unittest.main()
