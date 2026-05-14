import unittest

from app.screens.study_screen import (
    build_header_text,
    build_image_path,
    build_options_text,
    build_question_prompt,
)


class TestStudyScreen(unittest.TestCase):
    def test_build_question_prompt_for_review(self):
        question = {
            "type": "review",
            "field": "name_en",
            "options": ["Alanine", "Glycine", "Valine", "Serine"],
        }

        prompt = build_question_prompt(question)

        self.assertIn("name_en", prompt)

    def test_build_question_prompt_for_new(self):
        question = {
            "type": "new",
            "field": "abbr1",
        }

        prompt = build_question_prompt(question)

        self.assertIn("abbr1", prompt)

    def test_build_options_text_lists_choices(self):
        question = {
            "options": ["Alanine", "Glycine", "Valine", "Serine"],
        }

        text = build_options_text(question)

        self.assertIn("A.", text)
        self.assertIn("D.", text)

    def test_build_header_text_includes_plan_counts(self):
        plan = {"plan_date": "2026-05-13", "new_done": 1, "new_quota": 5, "review_done": 2}

        header = build_header_text(plan, index=0, total=3)

        self.assertIn("Plan 2026-05-13", header)
        self.assertIn("New 1/5", header)

    def test_build_image_path_returns_value(self):
        question = {"image_path": "/tmp/A.png"}

        path = build_image_path(question)

        self.assertEqual(path, "/tmp/A.png")


if __name__ == "__main__":
    unittest.main()
