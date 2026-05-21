"""Kivy app entrypoint."""

from __future__ import annotations

import os
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
except ModuleNotFoundError:
    App = object
    Label = None


class AminoStudyApp(App):
    def build(self):
        from app.bootstrap import bootstrap_storage
        from app.config import get_paths
        from app.runtime_assets import ensure_runtime_assets
        from app.screens.study_screen import (
            build_header_text,
            build_image_path,
            build_options_list,
            build_question_prompt,
            check_answer,
            load_study_state,
            submit_answer,
        )
        from app.services.reset import reset_progress

        if hasattr(self, "user_data_dir"):
            os.environ.setdefault("AMINO_DATA_DIR", self.user_data_dir)

        paths = get_paths()
        ensure_runtime_assets(data_dir=paths.data_dir, resource_root=paths.resource_root)
        bootstrap_storage(paths.db_path, paths.csv_path)

        if Label is None:
            return "Amino Study App"

        from app.fonts import resolve_ui_font

        font_selection = resolve_ui_font(resource_root=paths.resource_root)
        if font_selection.is_custom and font_selection.path is not None:
            LabelBase.register(name=font_selection.name, fn_regular=str(font_selection.path))

        ui_font_name = font_selection.name

        state = load_study_state(paths.db_path)

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
            height=72,
            font_name=ui_font_name,
            font_size=44,
            color=(0.7, 0.75, 0.8, 1),
        )

        card = BoxLayout(
            orientation="vertical",
            padding=24,
            spacing=12,
            size_hint_y=1,
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
            size_hint_y=0.40,
            font_name=ui_font_name,
            font_size=64,
            color=(0.12, 0.12, 0.12, 1),
        )

        options_box = BoxLayout(orientation="vertical", spacing=8, size_hint_y=0.30)
        row1 = BoxLayout(orientation="horizontal", spacing=8)
        row2 = BoxLayout(orientation="horizontal", spacing=8)
        option_buttons: list[Button] = []
        labels = ["A", "B", "C", "D"]
        for i, row in enumerate([row1, row2]):
            for j in range(2):
                btn = Button(
                    text="",
                    font_name=ui_font_name,
                    font_size=44,
                    background_color=(0.15, 0.4, 0.75, 1),
                    color=(1, 1, 1, 1),
                )
                option_buttons.append(btn)
                row.add_widget(btn)
        options_box.add_widget(row1)
        options_box.add_widget(row2)

        image_view = Image(size_hint_y=0.15, allow_stretch=True, keep_ratio=True)
        image_view.opacity = 0

        feedback_label = Label(
            text="",
            size_hint_y=0.07,
            font_name=ui_font_name,
            font_size=44,
            color=(0.12, 0.12, 0.12, 1),
        )
        feedback_label.opacity = 0

        next_button = Button(
            text="Next",
            size_hint_y=0.08,
            background_color=(0.85, 0.5, 0.1, 1),
            color=(1, 1, 1, 1),
            font_name=ui_font_name,
            font_size=44,
        )
        next_button.opacity = 0

        stats_label = Label(
            text="",
            size_hint_y=None,
            height=56,
            font_name=ui_font_name,
            font_size=40,
            color=(0.7, 0.75, 0.8, 1),
        )

        reset_button = Button(
            text="Reset progress",
            size_hint_y=None,
            height=56,
            background_color=(0.2, 0.2, 0.2, 1),
            color=(0.9, 0.9, 0.9, 1),
            font_name=ui_font_name,
            font_size=36,
        )

        answer_state = {"selected": None, "is_correct": False}

        def refresh_stats():
            p = state.plan
            stats_label.text = (
                f"New {p['new_done']}/{p['new_quota']} | Reviews {p['review_done']}"
            )

        def set_options_enabled(enabled: bool):
            for btn in option_buttons:
                btn.disabled = not enabled

        def show_answer_area():
            image_view.opacity = 1
            feedback_label.opacity = 1
            next_button.opacity = 1

        def hide_answer_area():
            image_view.opacity = 0
            feedback_label.opacity = 0
            next_button.opacity = 0

        def refresh_view():
            question = state.current_question()
            if not question:
                question_label.text = "Done! Come back tomorrow."
                for btn in option_buttons:
                    btn.text = ""
                set_options_enabled(False)
                hide_answer_area()
                header.text = build_header_text(state.plan, index=0, total=0)
                refresh_stats()
                return

            from datetime import date
            from app.db.learning_repo import get_daily_streak
            question["daily_streak"] = get_daily_streak(
                paths.db_path,
                amino_id=question["amino_id"],
                today=date.today().isoformat(),
            )

            header.text = build_header_text(
                state.plan, index=state.index, total=len(state.questions)
            )
            question_label.text = build_question_prompt(question)
            image_view.source = build_image_path(question)

            options = build_options_list(question)
            for i in range(4):
                if i < len(options):
                    option_buttons[i].text = f"{labels[i]}. {options[i]}"
                    option_buttons[i].background_color = (0.15, 0.4, 0.75, 1)
                else:
                    option_buttons[i].text = ""

            set_options_enabled(True)
            hide_answer_area()
            answer_state["selected"] = None
            answer_state["is_correct"] = False
            refresh_stats()

        def on_option_click(btn):
            if answer_state["selected"] is not None:
                return

            question = state.current_question()
            if not question:
                return

            selected_text = btn.text.split(". ", 1)[-1] if ". " in btn.text else btn.text
            is_correct = check_answer(question, selected_text)

            answer_state["selected"] = selected_text
            answer_state["is_correct"] = is_correct

            set_options_enabled(False)

            for b in option_buttons:
                if b is btn:
                    b.background_color = (0.15, 0.65, 0.15, 1) if is_correct else (0.85, 0.15, 0.15, 1)
                else:
                    option_text = b.text.split(". ", 1)[-1] if ". " in b.text else b.text
                    if option_text == question.get("answer", ""):
                        b.background_color = (0.15, 0.65, 0.15, 1)

            if is_correct:
                feedback_label.text = "Correct!"
                feedback_label.color = (0.15, 0.65, 0.15, 1)
            else:
                feedback_label.text = f"Incorrect. Answer: {question.get('answer', '')}"
                feedback_label.color = (0.85, 0.15, 0.15, 1)

            show_answer_area()

        def on_next(_instance):
            question = state.current_question()
            if not question:
                return

            is_correct = answer_state["is_correct"]

            submit_answer(
                paths.db_path,
                plan_id=state.plan_id,
                question=question,
                is_correct=is_correct,
            )

            state.advance()

            if state.index >= len(state.questions):
                state = load_study_state(paths.db_path)
                if not state.questions:
                    question_label.text = "Done! Come back tomorrow."
                    for btn in option_buttons:
                        btn.text = ""
                    set_options_enabled(False)
                    hide_answer_area()
                    header.text = build_header_text(state.plan, index=0, total=0)
                    refresh_stats()
                    return

            refresh_view()

        def on_reset(_instance):
            reset_progress(paths.db_path)
            nonlocal state
            state = load_study_state(paths.db_path)
            refresh_view()

        for btn in option_buttons:
            btn.bind(on_press=on_option_click)
        next_button.bind(on_press=on_next)
        reset_button.bind(on_press=on_reset)

        root.add_widget(header)
        card.add_widget(question_label)
        card.add_widget(options_box)
        card.add_widget(image_view)
        card.add_widget(feedback_label)
        card.add_widget(next_button)
        root.add_widget(card)
        root.add_widget(stats_label)
        root.add_widget(reset_button)

        refresh_view()
        return root


if __name__ == "__main__":
    AminoStudyApp().run()
