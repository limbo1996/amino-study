from __future__ import annotations

import csv
from pathlib import Path

REQUIRED_FIELDS = ("中文名", "英文名", "三字缩写", "单字缩写", "图片路径")


def load_amino_acids(csv_path: Path) -> list[dict]:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for field in REQUIRED_FIELDS:
            if field not in reader.fieldnames:
                raise ValueError(f"Missing required field: {field}")

        records = []
        for row in reader:
            record = {
                "name_cn": row["中文名"].strip(),
                "name_en": row["英文名"].strip(),
                "abbr3": row["三字缩写"].strip(),
                "abbr1": row["单字缩写"].strip(),
                "image_path": row["图片路径"].strip(),
                "formula": row.get("分子式", "").strip(),
            }
            records.append(record)

    return records
