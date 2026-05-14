"""Kivy app entrypoint."""

from __future__ import annotations

import sys
from pathlib import Path


def ensure_repo_root_on_path() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


ensure_repo_root_on_path()

try:
    from kivy.app import App
    from kivy.core.text import LabelBase
    from kivy.graphics import Color, Line, Rectangle
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.image import Image
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput
except ModuleNotFoundError:
    App = object
    Label = None


class AminoStudyApp(App):
    def build(self):
        from app.bootstrap import bootstrap_storage
        from app.config import CSV_PATH, DB_PATH, REPO_ROOT
        from app.screens.study_screen import (
            build_header_text,
            build_image_path,
            build_options_text,
            build_question_prompt,
            load_study_state,
            submit_answer,
        )
        from app.services.reset import reset_progress

        bootstrap_storage(DB_PATH, CSV_PATH)

        if Label is None:
            return "Amino Study App"

        display_font = REPO_ROOT / "skills/anthropics-skills/skills/canvas-design/canvas-fonts/Gloock-Regular.ttf"
        mono_font = REPO_ROOT / "skills/anthropics-skills/skills/canvas-design/canvas-fonts/RedHatMono-Regular.ttf"
        LabelBase.register(name="Gloock", fn_regular=str(display_font))
        LabelBase.register(name="RedHatMono", fn_regular=str(mono_font))

        state = load_study_state(DB_PATH)

        root = BoxLayout(orientation="vertical", padding=24, spacing=16)
        root.canvas.before.clear()
        with root.canvas.before:
            Color(0.08, 0.09, 0.12, 1)
            bg = Rectangle(pos=root.pos, size=root.size)

        def _update_bg(_instance, _value):
            bg.pos = root.pos
            bg.size = root.size

        root.bind(pos=_update_bg, size=_update_bg)

        header = Label(
            text="",
            size_hint_y=None,
            height=44,
            font_name="RedHatMono",
            font_size=16,
            color=(0.7, 0.75, 0.8, 1),
        )

        card = BoxLayout(
            orientation="vertical",
            padding=24,
            spacing=12,
            size_hint_y=None,
            height=360,
        )
        card.canvas.before.clear()
        with card.canvas.before:
            Color(0.94, 0.93, 0.9, 1)
            card_bg = Rectangle(pos=card.pos, size=card.size)
            Color(0.15, 0.15, 0.15, 1)
            card_border = Line(rectangle=(card.x, card.y, card.width, card.height), width=1.2)

        def _update_card(_instance, _value):
            card_bg.pos = card.pos
            card_bg.size = card.size
            card_border.rectangle = (card.x, card.y, card.width, card.height)

        card.bind(pos=_update_card, size=_update_card)

        question_label = Label(
            text="",
            size_hint_y=None,
            height=80,
            font_name="Gloock",
            font_size=26,
            color=(0.12, 0.12, 0.12, 1),
        )
        options_label = Label(
            text="",
            size_hint_y=None,
            height=140,
            font_name="RedHatMono",
            font_size=16,
            color=(0.12, 0.12, 0.12, 1),
        )
        image_view = Image(size_hint_y=None, height=160, allow_stretch=True, keep_ratio=True)
        answer_input = TextInput(
            text="",
            multiline=False,
            size_hint_y=None,
            height=44,
            font_name="RedHatMono",
            font_size=16,
            background_color=(0.98, 0.98, 0.96, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            cursor_color=(0.2, 0.2, 0.2, 1),
        )
        feedback_label = Label(
            text="",
            size_hint_y=None,
            height=32,
            font_name="RedHatMono",
            font_size=14,
            color=(0.85, 0.8, 0.55, 1),
        )
        next_button = Button(
            text="Submit",
            size_hint_y=None,
            height=48,
            background_color=(0.85, 0.5, 0.1, 1),
            color=(1, 1, 1, 1),
            font_name="RedHatMono",
            font_size=16,
        )

        stats_label = Label(
            text="New 0/5 | Reviews 0",
            size_hint_y=None,
            height=32,
            font_name="RedHatMono",
            font_size=14,
            color=(0.7, 0.75, 0.8, 1),
        )

        reset_button = Button(
            text="Reset progress",
            size_hint_y=None,
            height=40,
            background_color=(0.2, 0.2, 0.2, 1),
            color=(0.9, 0.9, 0.9, 1),
            font_name="RedHatMono",
            font_size=14,
        )

        def refresh_stats():
            p = state.plan
            stats_label.text = (
                f"New {p['new_done']}/{p['new_quota']} | Reviews {p['review_done']}"
            )

        def refresh_view():
            question = state.current_question()
            if not question:
                question_label.text = "No questions available"
                options_label.text = ""
                header.text = build_header_text(state.plan, index=0, total=0)
                refresh_stats()
                return
            header.text = build_header_text(
                state.plan, index=state.index, total=len(state.questions)
            )
            question_label.text = build_question_prompt(question)
            options_label.text = build_options_text(question)
            image_view.source = build_image_path(question)
            refresh_stats()

        def on_submit(_instance):
            question = state.current_question()
            if not question:
                return
            correct = submit_answer(
                DB_PATH,
                plan_id=state.plan_id,
                question=question,
                answer=answer_input.text,
            )
            feedback_label.text = "Correct" if correct else "Incorrect"
            state.advance()
            answer_input.text = ""
            refresh_view()

        def on_reset(_instance):
            reset_progress(DB_PATH)
            nonlocal state
            state = load_study_state(DB_PATH)
            refresh_view()

        next_button.bind(on_press=on_submit)
        reset_button.bind(on_press=on_reset)

        root.add_widget(header)
        card.add_widget(question_label)
        card.add_widget(image_view)
        card.add_widget(options_label)
        card.add_widget(answer_input)
        root.add_widget(card)
        root.add_widget(next_button)
        root.add_widget(feedback_label)
        root.add_widget(stats_label)
        root.add_widget(reset_button)

        refresh_view()
        return root


if __name__ == "__main__":
    AminoStudyApp().run()
