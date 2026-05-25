from __future__ import annotations

import csv
from pathlib import Path

REQUIRED_FIELDS = ("中文名", "英文名", "三字缩写", "单字缩写", "图片路径")

_EMBEDDED_DATA = [
    {"name_cn": "丙氨酸", "name_en": "Alanine", "abbr3": "Ala", "abbr1": "A", "filename": "A.png"},
    {"name_cn": "精氨酸", "name_en": "Arginine", "abbr3": "Arg", "abbr1": "R", "filename": "R.png"},
    {"name_cn": "天冬酰胺", "name_en": "Asparagine", "abbr3": "Asn", "abbr1": "N", "filename": "N.png"},
    {"name_cn": "天冬氨酸", "name_en": "Aspartic acid", "abbr3": "Asp", "abbr1": "D", "filename": "D.png"},
    {"name_cn": "半胱氨酸", "name_en": "Cysteine", "abbr3": "Cys", "abbr1": "C", "filename": "C.png"},
    {"name_cn": "谷氨酰胺", "name_en": "Glutamine", "abbr3": "Gln", "abbr1": "Q", "filename": "Q.png"},
    {"name_cn": "谷氨酸", "name_en": "Glutamic acid", "abbr3": "Glu", "abbr1": "E", "filename": "E.png"},
    {"name_cn": "甘氨酸", "name_en": "Glycine", "abbr3": "Gly", "abbr1": "G", "filename": "G.png"},
    {"name_cn": "组氨酸", "name_en": "Histidine", "abbr3": "His", "abbr1": "H", "filename": "H.png"},
    {"name_cn": "异亮氨酸", "name_en": "Isoleucine", "abbr3": "Ile", "abbr1": "I", "filename": "I.png"},
    {"name_cn": "亮氨酸", "name_en": "Leucine", "abbr3": "Leu", "abbr1": "L", "filename": "L.png"},
    {"name_cn": "赖氨酸", "name_en": "Lysine", "abbr3": "Lys", "abbr1": "K", "filename": "K.png"},
    {"name_cn": "甲硫氨酸", "name_en": "Methionine", "abbr3": "Met", "abbr1": "M", "filename": "M.png"},
    {"name_cn": "苯丙氨酸", "name_en": "Phenylalanine", "abbr3": "Phe", "abbr1": "F", "filename": "F.png"},
    {"name_cn": "脯氨酸", "name_en": "Proline", "abbr3": "Pro", "abbr1": "P", "filename": "P.png"},
    {"name_cn": "丝氨酸", "name_en": "Serine", "abbr3": "Ser", "abbr1": "S", "filename": "S.png"},
    {"name_cn": "苏氨酸", "name_en": "Threonine", "abbr3": "Thr", "abbr1": "T", "filename": "T.png"},
    {"name_cn": "色氨酸", "name_en": "Tryptophan", "abbr3": "Trp", "abbr1": "W", "filename": "W.png"},
    {"name_cn": "酪氨酸", "name_en": "Tyrosine", "abbr3": "Tyr", "abbr1": "Y", "filename": "Y.png"},
    {"name_cn": "缬氨酸", "name_en": "Valine", "abbr3": "Val", "abbr1": "V", "filename": "V.png"},
]


def load_amino_acids(csv_path: Path, *, repo_root: Path | None = None) -> list[dict]:
    if csv_path.exists():
        return _load_from_csv(csv_path, repo_root=repo_root)
    if repo_root is not None:
        csv_with_root = repo_root / csv_path.name
        if csv_with_root.exists():
            return _load_from_csv(csv_with_root, repo_root=repo_root)
    return _load_embedded(repo_root or Path.cwd())


def _load_from_csv(csv_path: Path, *, repo_root: Path | None) -> list[dict]:
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for field in REQUIRED_FIELDS:
            if field not in reader.fieldnames:
                raise ValueError(f"Missing required field: {field}")

        records = []
        for row in reader:
            image_path = row["图片路径"].strip()
            if repo_root is not None:
                image_path = str((repo_root / "fig" / Path(image_path).name))
            record = {
                "name_cn": row["中文名"].strip(),
                "name_en": row["英文名"].strip(),
                "abbr3": row["三字缩写"].strip(),
                "abbr1": row["单字缩写"].strip(),
                "image_path": image_path,
                "formula": row.get("分子式", "").strip(),
                "nature": row.get("性质", "").strip(),
            }
            records.append(record)
    return records


def _load_embedded(repo_root: Path) -> list[dict]:
    records = []
    for item in _EMBEDDED_DATA:
        records.append({
            "name_cn": item["name_cn"],
            "name_en": item["name_en"],
            "abbr3": item["abbr3"],
            "abbr1": item["abbr1"],
            "image_path": str(repo_root / "fig" / item["filename"]),
            "formula": "",
            "nature": "",
        })
    return records
