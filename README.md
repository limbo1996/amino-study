# Amino Study

A Kivy-based Android app for learning amino acid abbreviations through spaced-repetition flashcards and multiple-choice quizzes.

## Features

- 20 standard amino acids with Chinese/English names, 3-letter/1-letter abbreviations, and structural formulas
- Daily study plan with new/review quotas
- 5-day streak tracking per amino acid
- Multiple-choice quiz with random answer formats
- Spaced-repetition scheduling
- Progress reset support

## Quick Start (Desktop)

```bash
pip install kivy
python main.py
```

## Build for Android

```bash
buildozer android debug
```

The APK will be in `bin/`.

## Install on Android Emulator/Device

```bash
adb install -r bin/aminostudy-*-debug.apk
```

To uninstall:

```bash
adb uninstall com.example.aminostudy.aminostudy
```

## Project Structure

```
app/
  main.py          Kivy app entrypoint and UI
  screens/         Study, stats, settings screens
  services/        Quiz, session, plan, scheduler, reset logic
  db/              SQLite schema and learning repository
  data/            CSV data loader
  fonts.py         Font resolution for CJK support
assets/fonts/      Noto Sans SC bundled font
data/              Runtime data directory
fig/               Amino acid structural formula images
```

## Requirements

- Python 3.13+
- Kivy 2.3.1
- SQLite3
- Buildozer (for Android packaging)
