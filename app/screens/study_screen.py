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
    name_cn = question.get("name_cn", "").replace("[", "&bl;").replace("]", "&br;")
    name_en = question.get("name_en", "").replace("[", "&bl;").replace("]", "&br;")
    nature = question.get("nature", "").replace("[", "&bl;").replace("]", "&br;")
    streak = question.get("daily_streak", 0)
    return (
        f"[size=64]{name_cn} ({name_en})  进度：{streak}[/size]\n"
        f"[size=28]{nature}[/size]"
    )


def build_options_text(question: dict) -> str:
    options = question.get("options")
    if not options:
        return ""

    labels = ["A", "B", "C", "D"]
    lines = [f"{labels[i]}. {value}" for i, value in enumerate(options)]
    return "\n".join(lines)


def build_options_list(question: dict) -> list[str]:
    return list(question.get("options", []))


def check_answer(question: dict, selected: str) -> bool:
    return selected == question.get("answer", "")


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


def build_image_path(question: dict) -> str:
    return question.get("image_path", "")


def submit_answer(db_path, *, plan_id: int, question: dict, is_correct: bool) -> None:
    record_session_answer(
        db_path,
        plan_id=plan_id,
        question_type=question.get("type", ""),
        amino_id=question.get("amino_id"),
        is_correct=is_correct,
        now=datetime.now(),
    )
