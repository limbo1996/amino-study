from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable


def count_amino_acids(db_path: Path) -> int:
    with sqlite3.connect(db_path) as conn:
        return conn.execute("SELECT COUNT(*) FROM amino_acids").fetchone()[0]


def insert_amino_acids(db_path: Path, records: Iterable[dict]) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.executemany(
            """
            INSERT INTO amino_acids
            (name_cn, name_en, abbr3, abbr1, image_path, formula, nature)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    record["name_cn"],
                    record["name_en"],
                    record["abbr3"],
                    record["abbr1"],
                    record["image_path"],
                    record["formula"],
                    record.get("nature", ""),
                )
                for record in records
            ],
        )
        conn.commit()


def clear_amino_acids(db_path: Path) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM amino_acids")
        conn.commit()
