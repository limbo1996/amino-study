import unittest
from pathlib import Path


class TestModulePath(unittest.TestCase):
    def test_repo_root_added_to_sys_path(self):
        import sys

        from app.main import ensure_repo_root_on_path

        ensure_repo_root_on_path()
        repo_root = Path(__file__).resolve().parents[1]

        self.assertIn(str(repo_root), sys.path)


if __name__ == "__main__":
    unittest.main()
