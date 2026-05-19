"""Minimal Kivy app for Android runtime diagnostics."""

from __future__ import annotations

try:
    from kivy.app import App
    from kivy.uix.label import Label
except ModuleNotFoundError:
    App = object
    Label = None


class MinimalKivyApp(App):
    def build(self):
        if Label is None:
            return "Minimal Kivy App"
        return Label(text="Minimal Kivy App")


if __name__ == "__main__":
    MinimalKivyApp().run()
