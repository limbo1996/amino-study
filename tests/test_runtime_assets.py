import tempfile
import unittest
from pathlib import Path

from app.runtime_assets import ensure_runtime_assets


class TestRuntimeAssets(unittest.TestCase):
    def test_copies_csv_and_images(self):
        with tempfile.TemporaryDirectory() as resource_root, tempfile.TemporaryDirectory() as data_dir:
            resource_root_path = Path(resource_root)
            data_dir_path = Path(data_dir)

            csv_path = resource_root_path / "deepseek_csv_20260513_f1933c.csv"
            csv_path.write_text("中文名,英文名,三字缩写,单字缩写,图片路径\n丙氨酸,Alanine,Ala,A,fig/A.png\n", encoding="utf-8")

            fig_dir = resource_root_path / "fig"
            fig_dir.mkdir(parents=True)
            (fig_dir / "A.png").write_bytes(b"fake")

            ensure_runtime_assets(data_dir=data_dir_path, resource_root=resource_root_path)

            self.assertTrue((data_dir_path / "deepseek_csv_20260513_f1933c.csv").exists())
            self.assertTrue((data_dir_path / "fig" / "A.png").exists())


if __name__ == "__main__":
    unittest.main()
