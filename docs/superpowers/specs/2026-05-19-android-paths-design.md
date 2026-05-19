## Goal
Ensure the Android build does not crash on startup by moving all writable data to `App.user_data_dir` and copying bundled CSV/image resources into that directory on first run.

## Context
The desktop app reads and writes under the repo root. On Android, the packaged source directory is not guaranteed writable, which can fail during DB initialization or when reading resource paths from the CSV.

## Recommended Approach (A)
1. Compute a runtime data directory (prefer `App.user_data_dir`, allow env override for tests).
2. On startup, copy bundled CSV and `fig/*.png` to the data directory if missing.
3. Point DB and CSV paths to the data directory.
4. Normalize CSV image paths to the copied `fig/` directory.

## Data Flow
- `AminoStudyApp.build()` resolves the data directory and calls `ensure_runtime_assets()`.
- `ensure_runtime_assets()` copies CSV and images from the packaged resource root to `<data_dir>/`.
- `bootstrap_storage()` initializes DB at `<data_dir>/amino.db` and seeds from `<data_dir>/<csv>`.
- `load_amino_acids()` normalizes each `image_path` to `<data_dir>/fig/<basename>`.

## Error Handling
- Missing CSV or images: raise a clear `FileNotFoundError` during `ensure_runtime_assets()`.
- CSV schema mismatch: keep existing validation error for missing required fields.

## Testing Plan
- Unit test for config path resolution with env overrides.
- Unit test that `ensure_runtime_assets()` copies CSV and images into a temporary data directory.
- Unit test that CSV image paths are normalized to the target `fig` directory.

## Files to Change
- `app/config.py` (runtime data dir, paths, resource root)
- `app/runtime_assets.py` (new: copy logic)
- `app/main.py` (call ensure_runtime_assets before bootstrap)
- `app/data/loader.py` (normalize image paths)
- `tests/test_config_paths.py` (update for new behavior)
- `tests/test_runtime_assets.py` (new)
- `tests/test_data_loader.py` (update image path normalization)
- `buildozer.spec` (verify CSV and fig included)
