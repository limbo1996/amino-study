from __future__ import annotations

import sqlite3
from pathlib import Path


def init_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS amino_acids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_cn TEXT NOT NULL,
                name_en TEXT NOT NULL,
                abbr3 TEXT NOT NULL,
                abbr1 TEXT NOT NULL,
                image_path TEXT NOT NULL,
                formula TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS learning_state (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amino_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                last_seen_at TEXT,
                next_review_at TEXT,
                wrong_count INTEGER NOT NULL DEFAULT 0,
                right_streak INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (amino_id) REFERENCES amino_acids(id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS daily_plan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plan_date TEXT NOT NULL,
                new_quota INTEGER NOT NULL,
                new_done INTEGER NOT NULL DEFAULT 0,
                review_done INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.commit()
