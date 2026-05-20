from __future__ import annotations

from pathlib import Path

from app.db.schema import init_db, migrate_add_daily_streak
from app.services.seed import ensure_seeded


def bootstrap_storage(db_path: Path, csv_path: Path) -> bool:
    init_db(db_path)
    migrate_add_daily_streak(db_path)
    return ensure_seeded(db_path, csv_path)
