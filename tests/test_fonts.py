import tempfile
import unittest
from pathlib import Path


class TestFontSelection(unittest.TestCase):
    def test_resolve_ui_font_prefers_bundled_font(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            font_path = root / "assets" / "fonts" / "NotoSansSC-Regular.ttf"
            font_path.parent.mkdir(parents=True, exist_ok=True)
            font_path.write_bytes(b"")

            from app.fonts import resolve_ui_font

            selection = resolve_ui_font(resource_root=root)

            self.assertEqual(selection.name, "NotoSansSC")
            self.assertEqual(selection.path, font_path)
            self.assertTrue(selection.is_custom)

    def test_resolve_ui_font_falls_back_to_roboto(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            from app.fonts import resolve_ui_font

            selection = resolve_ui_font(resource_root=root)

            self.assertEqual(selection.name, "Roboto")
            self.assertIsNone(selection.path)
            self.assertFalse(selection.is_custom)


if __name__ == "__main__":
    unittest.main()
