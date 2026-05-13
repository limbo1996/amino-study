import unittest


class TestAppEntry(unittest.TestCase):
    def test_build_returns_root_widget(self):
        from app.main import AminoStudyApp

        app = AminoStudyApp()
        root = app.build()

        self.assertIsNotNone(root)


if __name__ == "__main__":
    unittest.main()
