from __future__ import annotations

import platform
import traceback
from datetime import datetime, timezone
from pathlib import Path


def write_crash_log(*, data_dir: Path, error: BaseException, context: dict | None = None) -> Path:
    data_dir.mkdir(parents=True, exist_ok=True)
    log_path = data_dir / "crash.log"

    header = [
        f"timestamp={datetime.now(timezone.utc).isoformat()}",
        f"platform={platform.platform()}",
        f"python={platform.python_version()}",
    ]
    if context:
        for key, value in context.items():
            header.append(f"{key}={value}")

    with log_path.open("w", encoding="utf-8") as handle:
        handle.write("\n".join(header))
        handle.write("\n\n")
        handle.write("".join(traceback.format_exception(type(error), error, error.__traceback__)))

    return log_path
