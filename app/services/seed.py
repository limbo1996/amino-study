from __future__ import annotations

from pathlib import Path

from app.data.loader import load_amino_acids
from app.db.repo import clear_amino_acids, count_amino_acids, insert_amino_acids


def ensure_seeded(db_path: Path, csv_path: Path) -> bool:
    if count_amino_acids(db_path) > 0:
        return False

    records = load_amino_acids(csv_path)
    insert_amino_acids(db_path, records)
    return True


def reload_seed_data(db_path: Path, csv_path: Path) -> None:
    records = load_amino_acids(csv_path)
    clear_amino_acids(db_path)
    insert_amino_acids(db_path, records)
