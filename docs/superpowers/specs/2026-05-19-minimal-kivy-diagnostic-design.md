## Goal
Build a minimal Kivy APK that only shows a basic label, to verify that Kivy launches correctly on Android 16 (Dimensity 9500) independent of app logic.

## Context
The current APK crashes before Python entrypoint (no app data dir created, no crash log). A minimal Kivy build isolates whether the failure is in the native/runtime layer or in the app code/resources.

## Recommended Approach
1. Create a minimal Kivy app entry that only renders a label.
2. Use a separate build profile or temporary entrypoint to package the minimal app.
3. Build a debug APK and install for device test.

## Scope
- No CSV/DB/image assets.
- No runtime asset copying.
- No app services or custom UI.

## Success Criteria
- APK installs and opens to a simple label screen without crashing.
- If it still crashes, we focus on build/runtime/ABI/toolchain settings.

## Files to Change
- `main.py` (temporary minimal entrypoint) or add `main_minimal.py` and switch `buildozer.spec` for the diagnostic build.
- `buildozer.spec` (if entrypoint switch is needed for diagnostic build).

## Testing Plan
- Build `buildozer android debug`.
- Install APK and confirm app opens and renders label.
