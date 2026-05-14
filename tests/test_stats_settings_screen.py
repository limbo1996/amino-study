import unittest

from app.screens.stats_screen import build_stats_text
from app.screens.settings_screen import build_reset_label


class TestStatsSettingsScreen(unittest.TestCase):
    def test_build_stats_text_includes_counts(self):
        stats = {"new_done": 2, "new_quota": 5, "review_done": 3}

        text = build_stats_text(stats)

        self.assertIn("New 2/5", text)
        self.assertIn("Reviews 3", text)

    def test_build_reset_label_mentions_reset(self):
        label = build_reset_label()

        self.assertIn("Reset", label)


if __name__ == "__main__":
    unittest.main()
