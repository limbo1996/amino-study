import unittest

from app.screens.study_screen import (
    build_header_text,
    build_image_path,
    build_options_list,
    build_options_text,
    build_question_prompt,
    check_answer,
)


class TestStudyScreen(unittest.TestCase):
    def test_build_question_prompt_for_review(self):
        question = {
            "type": "choice",
            "name_cn": "丙氨酸",
            "name_en": "Alanine",
            "options": ["Ala", "Gly", "Val", "Ser"],
        }

        prompt = build_question_prompt(question)

        self.assertIn("丙氨酸", prompt)
        self.assertIn("Alanine", prompt)

    def test_build_question_prompt_for_new(self):
        question = {
            "type": "choice",
            "name_cn": "甘氨酸",
            "name_en": "Glycine",
        }

        prompt = build_question_prompt(question)

        self.assertIn("甘氨酸", prompt)
        self.assertIn("Glycine", prompt)

    def test_build_options_text_lists_choices(self):
        question = {
            "options": ["Ala", "Gly", "Val", "Ser"],
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

    def test_build_options_list_returns_four_values(self):
        question = {"options": ["Ala", "Gly", "Val", "Ser"]}

        result = build_options_list(question)

        self.assertEqual(result, ["Ala", "Gly", "Val", "Ser"])
        self.assertEqual(len(result), 4)

    def test_build_question_prompt_includes_nature_on_second_line(self):
        question = {
            "type": "choice",
            "name_cn": "丙氨酸",
            "name_en": "Alanine",
            "nature": "非极性脂肪族",
        }

        prompt = build_question_prompt(question)

        self.assertIn("[size=64]", prompt)
        self.assertIn("丙氨酸", prompt)
        self.assertIn("[size=28]", prompt)
        self.assertIn("非极性脂肪族", prompt)
        self.assertIn("\n", prompt)

    def test_build_question_prompt_escapes_markup_brackets(self):
        question = {
            "type": "choice",
            "name_cn": "测试[data]",
            "name_en": "test",
            "nature": "性质[info]",
        }

        prompt = build_question_prompt(question)

        self.assertNotIn("测试[data]", prompt)
        self.assertNotIn("性质[info]", prompt)
        self.assertIn("&bl;", prompt)
        self.assertIn("&br;", prompt)

    def test_build_question_prompt_without_nature_shows_empty_second_line(self):
        question = {
            "type": "choice",
            "name_cn": "甘氨酸",
            "name_en": "Glycine",
        }

        prompt = build_question_prompt(question)

        self.assertIn("甘氨酸", prompt)
        self.assertIn("[size=28]", prompt)

    def test_check_answer_correct(self):
        question = {"answer": "Ala"}

        self.assertTrue(check_answer(question, "Ala"))

    def test_check_answer_incorrect(self):
        question = {"answer": "Ala"}

        self.assertFalse(check_answer(question, "Gly"))


if __name__ == "__main__":
    unittest.main()
