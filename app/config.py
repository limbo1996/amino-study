from __future__ import annotations

import os
from pathlib import Path


def _find_repo_root() -> Path:
    approaches = [
        lambda: Path(__file__).resolve().parents[1],
        lambda: Path(os.path.dirname(os.path.abspath(__file__))).parents[1],
        lambda: Path(os.path.dirname(os.path.abspath(__file__))).parent,
        lambda: Path.cwd(),
    ]
    for fn in approaches:
        try:
            root = fn()
            if (root / "fig").is_dir() or (root / "fig").exists():
                return root
        except Exception:
            continue
    return Path.cwd()


REPO_ROOT = _find_repo_root()
DB_PATH = REPO_ROOT / "data" / "amino.db"
CSV_PATH = REPO_ROOT / "deepseek_csv_20260513_f1933c.csv"
