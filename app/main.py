"""Kivy app entrypoint."""

try:
    from kivy.app import App
    from kivy.uix.label import Label
except ModuleNotFoundError:
    App = object
    Label = None


class AminoStudyApp(App):
    def build(self):
        if Label is None:
            return "Amino Study App"
        return Label(text="Amino Study App")


if __name__ == "__main__":
    AminoStudyApp().run()
