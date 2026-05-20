## Goal
- Prevent Android startup crash caused by `Label.font_name=None` by packaging a CJK-capable font and using a safe fallback path.

## Context
- Current crash: `ValueError: None is not allowed for Label.font_name` when fonts are missing.
- App runs on Android via Kivy/Buildozer; needs consistent font availability across devices.

## Requirements
- Bundle a Chinese-capable font (recommended: Noto Sans SC).
- Register the font at startup and use it for all labels/buttons.
- Never pass `None` to `font_name`.
- If the font file is missing, fall back to a built-in font (Roboto) and log the fallback.

## Design
- Add `NotoSansSC` font files under `assets/fonts/` and ensure they are packaged.
- Register the font with `LabelBase.register(name="NotoSansSC", fn_regular=...)`.
- Replace per-widget `font_name` values with a single `ui_font_name` that is:
  - `NotoSansSC` when the bundled font is present.
  - `Roboto` as a guaranteed fallback.
- Keep layout, colors, and logic unchanged.

## Error Handling
- If the font file does not exist at runtime, log a warning and use `Roboto`.

## Testing
- Add or update a unit test to assert the font path is resolved and that `font_name` is never `None`.
- Manual: launch APK on emulator and verify no crash at startup.

## Out of Scope
- UI redesign or typography tuning beyond font availability.
