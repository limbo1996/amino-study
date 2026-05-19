import tempfile
import unittest
from pathlib import Path

from app.crash_logging import write_crash_log


class TestCrashLogging(unittest.TestCase):
    def test_writes_crash_log(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            log_path = write_crash_log(
                data_dir=temp_path,
                error=RuntimeError("boom"),
                context={"data_dir": str(temp_path)},
            )

            self.assertTrue(log_path.exists())
            content = log_path.read_text(encoding="utf-8")
            self.assertIn("RuntimeError", content)
            self.assertIn("boom", content)


if __name__ == "__main__":
    unittest.main()
