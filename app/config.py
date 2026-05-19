from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RuntimePaths:
    data_dir: Path
    db_path: Path
    csv_path: Path
    resource_root: Path


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


def _safe_resource_root() -> Path:
    env_root = os.environ.get("AMINO_RESOURCE_ROOT")
    if env_root:
        return Path(env_root)
    return _find_repo_root()


def _safe_data_dir() -> Path:
    env_dir = os.environ.get("AMINO_DATA_DIR")
    if env_dir:
        return Path(env_dir)
    return _find_repo_root() / "data"


def get_paths() -> RuntimePaths:
    data_dir = _safe_data_dir()
    resource_root = _safe_resource_root()
    return RuntimePaths(
        data_dir=data_dir,
        db_path=data_dir / "amino.db",
        csv_path=data_dir / "deepseek_csv_20260513_f1933c.csv",
        resource_root=resource_root,
    )


PATHS = get_paths()
REPO_ROOT = _safe_resource_root()
DB_PATH = PATHS.db_path
CSV_PATH = PATHS.csv_path
