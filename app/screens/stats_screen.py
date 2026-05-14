from __future__ import annotations


def build_stats_text(stats: dict) -> str:
    return (
        f"New {stats.get('new_done', 0)}/{stats.get('new_quota', 0)} "
        f"| Reviews {stats.get('review_done', 0)}"
    )
