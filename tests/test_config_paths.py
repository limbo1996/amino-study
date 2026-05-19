import os
import tempfile
import unittest
from pathlib import Path

from app.config import get_paths


class TestConfigPaths(unittest.TestCase):
    def test_paths_use_env_overrides(self):
        with tempfile.TemporaryDirectory() as temp_data, tempfile.TemporaryDirectory() as temp_resource:
            os.environ["AMINO_DATA_DIR"] = temp_data
            os.environ["AMINO_RESOURCE_ROOT"] = temp_resource

            paths = get_paths()

            self.assertEqual(paths.data_dir, Path(temp_data))
            self.assertEqual(paths.db_path, Path(temp_data) / "amino.db")
            self.assertEqual(paths.csv_path, Path(temp_data) / "deepseek_csv_20260513_f1933c.csv")
            self.assertEqual(paths.resource_root, Path(temp_resource))


if __name__ == "__main__":
    unittest.main()
