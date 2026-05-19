import unittest


class TestMinimalEntry(unittest.TestCase):
    def test_minimal_app_builds(self):
        from minimal_app import MinimalKivyApp

        app = MinimalKivyApp()
        root = app.build()

        self.assertIsNotNone(root)


if __name__ == "__main__":
    unittest.main()
