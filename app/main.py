"""Kivy app entrypoint."""

try:
    from kivy.app import App
    from kivy.uix.label import Label
except ModuleNotFoundError:
    App = object
    Label = None


class AminoStudyApp(App):
    def build(self):
        from app.bootstrap import bootstrap_storage
        from app.config import CSV_PATH, DB_PATH

        bootstrap_storage(DB_PATH, CSV_PATH)

        if Label is None:
            return "Amino Study App"
        return Label(text="Amino Study App")


if __name__ == "__main__":
    AminoStudyApp().run()
