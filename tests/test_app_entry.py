import os
import tempfile
import unittest
from pathlib import Path


class TestAppEntry(unittest.TestCase):
    def test_build_returns_root_widget(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            data_dir = temp_path / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            fig_dir = data_dir / "fig"
            fig_dir.mkdir(parents=True, exist_ok=True)

            repo_root = Path(__file__).resolve().parents[1]
            csv_path = repo_root / "deepseek_csv_20260513_f1933c.csv"
            if csv_path.exists():
                (data_dir / csv_path.name).write_text(csv_path.read_text(encoding="utf-8"), encoding="utf-8")

            sample_png = next((repo_root / "fig").glob("*.png"), None)
            if sample_png is not None:
                (fig_dir / sample_png.name).write_bytes(sample_png.read_bytes())

            os.environ["AMINO_DATA_DIR"] = str(data_dir)
            os.environ["AMINO_RESOURCE_ROOT"] = str(repo_root)

            from app.main import AminoStudyApp

            app = AminoStudyApp()
            root = app.build()

            self.assertIsNotNone(root)


if __name__ == "__main__":
    unittest.main()
