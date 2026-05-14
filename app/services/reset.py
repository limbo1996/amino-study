from __future__ import annotations

import sqlite3
from pathlib import Path


def reset_progress(db_path: Path) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM learning_state")
        conn.execute("DELETE FROM daily_plan")
        conn.commit()
