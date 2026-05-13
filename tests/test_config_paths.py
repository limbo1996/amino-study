import unittest
from pathlib import Path

from app import config


class TestConfigPaths(unittest.TestCase):
    def test_paths_resolve_within_repo(self):
        self.assertTrue(config.REPO_ROOT.is_dir())
        self.assertTrue(str(config.DB_PATH).startswith(str(config.REPO_ROOT)))
        self.assertTrue(str(config.CSV_PATH).startswith(str(config.REPO_ROOT)))

    def test_data_directory_exists(self):
        self.assertTrue(config.DB_PATH.parent.is_dir())
        self.assertEqual(config.DB_PATH.parent, config.REPO_ROOT / "data")


if __name__ == "__main__":
    unittest.main()
