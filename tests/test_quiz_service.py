import unittest

from app.services.quiz import generate_abbr_question


class TestQuizService(unittest.TestCase):
    def test_abbr_question_uses_single_format(self):
        items = [
            {"id": 1, "abbr3": "Ala", "abbr1": "A"},
            {"id": 2, "abbr3": "Gly", "abbr1": "G"},
            {"id": 3, "abbr3": "Val", "abbr1": "V"},
            {"id": 4, "abbr3": "Ser", "abbr1": "S"},
        ]

        question = generate_abbr_question(items, correct_index=0, format_type="abbr1")

        self.assertEqual(question["format"], "abbr1")
        self.assertEqual(len(question["options"]), 4)
        self.assertEqual(len(set(question["options"])), 4)
        self.assertIn("A", question["options"])

    def test_abbr_question_returns_three_letter_format(self):
        items = [
            {"id": 1, "abbr3": "Ala", "abbr1": "A"},
            {"id": 2, "abbr3": "Gly", "abbr1": "G"},
            {"id": 3, "abbr3": "Val", "abbr1": "V"},
            {"id": 4, "abbr3": "Ser", "abbr1": "S"},
        ]

        question = generate_abbr_question(items, correct_index=2, format_type="abbr3")

        self.assertEqual(question["answer"], "Val")
        self.assertTrue(all(len(option) == 3 for option in question["options"]))

    def test_abbr_question_random_format_per_call(self):
        items = [
            {"id": 1, "abbr3": "Ala", "abbr1": "A"},
            {"id": 2, "abbr3": "Gly", "abbr1": "G"},
            {"id": 3, "abbr3": "Val", "abbr1": "V"},
            {"id": 4, "abbr3": "Ser", "abbr1": "S"},
            {"id": 5, "abbr3": "Leu", "abbr1": "L"},
        ]

        formats = set()
        for _ in range(10):
            question = generate_abbr_question(items, correct_index=0, format_type=None)
            formats.add(question["format"])

        self.assertIn("abbr1", formats)
        self.assertIn("abbr3", formats)


if __name__ == "__main__":
    unittest.main()
