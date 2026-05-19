from __future__ import annotations

import shutil
from pathlib import Path


def _copy_file(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def ensure_runtime_assets(*, data_dir: Path, resource_root: Path) -> None:
    csv_name = "deepseek_csv_20260513_f1933c.csv"
    csv_src = resource_root / csv_name
    if not csv_src.exists():
        raise FileNotFoundError(f"Missing resource CSV: {csv_src}")

    csv_dest = data_dir / csv_name
    if not csv_dest.exists():
        _copy_file(csv_src, csv_dest)

    fig_src = resource_root / "fig"
    if not fig_src.exists():
        raise FileNotFoundError(f"Missing resource fig directory: {fig_src}")

    fig_dest = data_dir / "fig"
    fig_dest.mkdir(parents=True, exist_ok=True)

    for image in fig_src.glob("*.png"):
        target = fig_dest / image.name
        if not target.exists():
            _copy_file(image, target)
