import unittest

from app.services.quiz import generate_fill_in, generate_multiple_choice


class TestQuizService(unittest.TestCase):
    def test_multiple_choice_contains_correct_answer(self):
        items = [
            {"id": 1, "name_en": "Alanine"},
            {"id": 2, "name_en": "Glycine"},
            {"id": 3, "name_en": "Valine"},
            {"id": 4, "name_en": "Serine"},
        ]

        question = generate_multiple_choice(items, field="name_en", correct_index=0)

        self.assertEqual(question["answer"], "Alanine")
        self.assertEqual(len(question["options"]), 4)
        self.assertEqual(len(set(question["options"])), 4)
        self.assertIn("Alanine", question["options"])

    def test_fill_in_returns_prompt_and_answer(self):
        item = {"name_cn": "丙氨酸", "abbr1": "A"}

        question = generate_fill_in(item, field="abbr1")

        self.assertEqual(question["answer"], "A")
        self.assertIn("prompt", question)


if __name__ == "__main__":
    unittest.main()
