"""Android entry point — delegates to app.main."""

import traceback
import sys

if __name__ == "__main__":
    try:
        from app.main import AminoStudyApp
        AminoStudyApp().run()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
