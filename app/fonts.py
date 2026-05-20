from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FontSelection:
    name: str
    path: Path | None
    is_custom: bool


def resolve_ui_font(*, resource_root: Path) -> FontSelection:
    font_path = resource_root / "assets" / "fonts" / "NotoSansSC-Regular.ttf"
    if font_path.exists():
        return FontSelection(name="NotoSansSC", path=font_path, is_custom=True)
    return FontSelection(name="Roboto", path=None, is_custom=False)
