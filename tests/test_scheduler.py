import unittest
from datetime import datetime, timedelta

from app.services.scheduler import (
    compute_next_review,
    prioritize_due_reviews,
)


class TestScheduler(unittest.TestCase):
    def test_compute_next_review_correct_advances_interval(self):
        now = datetime(2026, 5, 13, 9, 0, 0)

        next_review, next_streak, next_wrong = compute_next_review(
            now=now,
            right_streak=0,
            wrong_count=0,
            is_correct=True,
        )

        self.assertEqual(next_review, now + timedelta(days=1))
        self.assertEqual(next_streak, 1)
        self.assertEqual(next_wrong, 0)

    def test_compute_next_review_incorrect_resets_streak(self):
        now = datetime(2026, 5, 13, 9, 0, 0)

        next_review, next_streak, next_wrong = compute_next_review(
            now=now,
            right_streak=3,
            wrong_count=1,
            is_correct=False,
        )

        self.assertEqual(next_review, now + timedelta(days=1))
        self.assertEqual(next_streak, 0)
        self.assertEqual(next_wrong, 2)

    def test_compute_next_review_caps_interval(self):
        now = datetime(2026, 5, 13, 9, 0, 0)

        next_review, next_streak, next_wrong = compute_next_review(
            now=now,
            right_streak=5,
            wrong_count=0,
            is_correct=True,
        )

        self.assertEqual(next_review, now + timedelta(days=15))
        self.assertEqual(next_streak, 6)
        self.assertEqual(next_wrong, 0)

    def test_prioritize_due_reviews_orders_by_wrong_count(self):
        now = datetime(2026, 5, 13, 9, 0, 0)
        items = [
            {
                "id": 1,
                "next_review_at": now - timedelta(days=1),
                "wrong_count": 1,
            },
            {
                "id": 2,
                "next_review_at": now - timedelta(days=2),
                "wrong_count": 3,
            },
            {
                "id": 3,
                "next_review_at": now + timedelta(days=1),
                "wrong_count": 10,
            },
        ]

        ordered = prioritize_due_reviews(items, now=now)
        ordered_ids = [item["id"] for item in ordered]

        self.assertEqual(ordered_ids, [2, 1])


if __name__ == "__main__":
    unittest.main()
