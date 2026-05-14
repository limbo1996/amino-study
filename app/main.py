"""Kivy app entrypoint."""

try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput
except ModuleNotFoundError:
    App = object
    Label = None


class AminoStudyApp(App):
    def build(self):
        from app.bootstrap import bootstrap_storage
        from app.config import CSV_PATH, DB_PATH
        from app.screens.study_screen import (
            build_header_text,
            build_options_text,
            build_question_prompt,
            load_study_state,
            submit_answer,
        )

        bootstrap_storage(DB_PATH, CSV_PATH)

        if Label is None:
            return "Amino Study App"

        state = load_study_state(DB_PATH)

        root = BoxLayout(orientation="vertical", padding=12, spacing=8)
        header = Label(text="", size_hint_y=None, height=40)
        question_label = Label(text="", size_hint_y=None, height=60)
        options_label = Label(text="", size_hint_y=None, height=120)
        answer_input = TextInput(text="", multiline=False, size_hint_y=None, height=40)
        feedback_label = Label(text="", size_hint_y=None, height=40)
        next_button = Button(text="Submit", size_hint_y=None, height=44)

        def refresh_view():
            question = state.current_question()
            if not question:
                question_label.text = "No questions available"
                options_label.text = ""
                header.text = build_header_text(state.plan, index=0, total=0)
                return
            header.text = build_header_text(
                state.plan, index=state.index, total=len(state.questions)
            )
            question_label.text = build_question_prompt(question)
            options_label.text = build_options_text(question)

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

        next_button.bind(on_press=on_submit)

        root.add_widget(header)
        root.add_widget(question_label)
        root.add_widget(options_label)
        root.add_widget(answer_input)
        root.add_widget(next_button)
        root.add_widget(feedback_label)

        refresh_view()
        return root


if __name__ == "__main__":
    AminoStudyApp().run()
