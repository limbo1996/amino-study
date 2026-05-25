# AGENTS.md

## Commands

```bash
# Desktop run
python main.py

# Run all tests
python -m unittest discover tests

# Run single test file
python -m unittest tests.test_quiz_service

# Android debug build
buildozer android debug

# Android diagnostics/minimal build (arm64-v8a only)
buildozer --profile minimal android debug

# Install APK on device/emulator
adb install -r bin/aminostudy-*-debug.apk

# Uninstall
adb uninstall com.example.aminostudy.aminostudy
```

## Architecture

- **Kivy Android app** with SQLite local storage. No server, no network.
- `main.py` — Android crash-guarded entrypoint; delegates to `app.main.AminoStudyApp`
- `minimal_app.py` — standalone diagnostics entrypoint (used with buildozer `minimal` profile)
- `app/` — Kivy app package: `main.py` (UI), `config.py` (paths), `bootstrap.py` (DB init + seed), `runtime_assets.py` (copy CSV/images to data dir)
  - `app/screens/` — study_screen, stats_screen, settings_screen
  - `app/services/` — plan, quiz, session, seed, scheduler, reset
  - `app/db/` — schema (init_db, migrate_add_daily_streak), learning_repo
  - `app/data/` — CSV loader
- `fig/` — amino acid structural formula PNGs (named `A.png`, `C.png`, etc.)
- `data/` — runtime data directory (auto-created, gitignored except CSV)
- `assets/fonts/` — Noto Sans SC bundled CJK font
- `prd.json` — Ralph-format PRD for the current feature (5-streak daily progress)
- `init/` — empty; no active purpose

## No build/lint/typecheck tooling

No `setup.py`, `pyproject.toml`, `requirements.txt`, `Makefile`, CI, or pre-commit hooks. Kivy is imported at runtime with a guard:

```python
try:
    from kivy.app import App
except ModuleNotFoundError:
    App = object
```

Tests must not import Kivy at module level, or must use this same guard.

## Path resolution

Two env var overrides (set before imports):
- `AMINO_DATA_DIR` — where DB, CSV, and fig/ are copied at runtime
- `AMINO_RESOURCE_ROOT` — where fig/ and CSV are read from during bootstrap

Auto-detection finds repo root by locating the `fig/` directory.

## Kivy platform gotchas

1. **Never dynamically change `size_hint_y`** on Android — BoxLayout re-layouts and widgets disappear/relocate. Use `opacity` to toggle visibility instead.
2. **Never pass `None` to `Label.font_name`** — triggers `ValueError` on Android. Always resolve font: check `assets/fonts/NotoSansSC-Regular.ttf` exists, fall back to `"Roboto"`.
3. Resources (CSV, fig/*.png, fonts) must be in `source.include_patterns` in `buildozer.spec` to be packaged in APK.

## Buildozer quirks

- `p4a.branch = develop` (non-default)
- `android.archs` defaults to all; `minimal` profile limits to `arm64-v8a`
- `source.exclude_dirs` excludes `tests, bin, venv, skills, docs`

## Database

- SQLite at `data/amino.db` (created by `app/db/schema.py:init_db()`)
- Tables: `amino_acids`, `learning_state`, `daily_plan`
- `migrate_add_daily_streak()` catches `sqlite3.OperationalError` — idempotent re-runs

## Testing

- Standard `unittest`; no pytest, no fixtures
- Each test creates temp dirs and DBs — no shared state
- Tests use `tests/test_*.py` naming convention
- Many tests seed `amino_acids` and/or `learning_state` rows manually before asserting

## Workflow rules

Every code change must follow this sequence:
1. `brainstorming` skill
2. `planning-with-files-zh` skill
3. `test-driven-development` skill
4. `ralph` skill (confirmation)

UI/visual design work must use the `frontend-design` skill.

Each change must be committed with a clear git commit message.
