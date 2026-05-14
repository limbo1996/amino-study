from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.services.session import build_session, record_session_answer


def build_header_text(plan: dict, *, index: int, total: int) -> str:
    return (
        f"Plan {plan['plan_date']} | New {plan['new_done']}/{plan['new_quota']} "
        f"| Reviews {plan['review_done']} | Q {index + 1}/{max(total, 1)}"
    )


def build_question_prompt(question: dict) -> str:
    q_type = question.get("type", "")
    field = question.get("field", "")
    return f"{q_type} question: {field}"


def build_options_text(question: dict) -> str:
    options = question.get("options")
    if not options:
        return ""

    labels = ["A", "B", "C", "D"]
    lines = [f"{labels[i]}. {value}" for i, value in enumerate(options)]
    return "\n".join(lines)


@dataclass
class StudyState:
    plan: dict
    plan_id: int
    questions: list[dict]
    index: int = 0

    def current_question(self) -> dict | None:
        if not self.questions:
            return None
        if self.index >= len(self.questions):
            return None
        return self.questions[self.index]

    def advance(self) -> None:
        if self.index < len(self.questions):
            self.index += 1


def load_study_state(db_path) -> StudyState:
    session = build_session(db_path, now=datetime.now())
    return StudyState(
        plan=session["plan"],
        plan_id=session["plan"]["id"],
        questions=session["questions"],
    )


def submit_answer(db_path, *, plan_id: int, question: dict, answer: str) -> bool:
    correct = answer.strip() == str(question.get("answer", "")).strip()
    record_session_answer(
        db_path,
        plan_id=plan_id,
        question_type=question.get("type", ""),
        amino_id=question.get("amino_id"),
        is_correct=correct,
        now=datetime.now(),
    )
    return correct
