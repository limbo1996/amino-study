"""Android entry point — delegates to app.main."""

import os
import sys
import traceback
from pathlib import Path

from app.crash_logging import write_crash_log


def _safe_data_dir() -> Path:
    env_dir = os.environ.get("AMINO_DATA_DIR")
    if env_dir:
        return Path(env_dir)
    return Path.cwd() / "data"


if __name__ == "__main__":
    try:
        from app.main import AminoStudyApp

        AminoStudyApp().run()
    except Exception as exc:
        try:
            write_crash_log(
                data_dir=_safe_data_dir(),
                error=exc,
                context={
                    "data_dir": str(_safe_data_dir()),
                    "resource_root": os.environ.get("AMINO_RESOURCE_ROOT", ""),
                },
            )
        except Exception:
            pass
        traceback.print_exc()
        sys.exit(1)
