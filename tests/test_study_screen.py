import unittest

from app.screens.study_screen import build_options_text, build_question_prompt


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


if __name__ == "__main__":
    unittest.main()
