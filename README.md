# Amino Study

一个闲来无事完全 Vibe Coding 的氨基酸记忆 APP。

> 所有内容包括本README，完全由AI生成。
>
> 使用工具：opencode + Github Copilot +DeepSeek V4 Pro

## Features

- 20 amino acids with Chinese/English names, abbreviations, chemical properties, and structure images
- Daily study plan with automated new/review item scheduling
- 5-streak daily progress: require 5 consecutive correct answers per amino acid to mark as learned
- Property display: shows each amino acid's chemical nature (polarity, charge) on the quiz screen
- Spaced-repetition scheduling with wrong-count and right-streak tracking
- Progress reset and statistics

## Quick Start

```bash
pip install kivy
python main.py
```

## Android

### Build

```bash
buildozer android debug
```

### Install

```bash
adb install -r bin/aminostudy-*-debug.apk
adb uninstall com.example.aminostudy.aminostudy   # uninstall
```

## Testing

```bash
python -m unittest discover tests
python -m unittest tests.test_quiz_service         # single file
```

## Structure

```
app/
  main.py              Kivy app entrypoint and UI
  screens/             study_screen, stats_screen, settings_screen
  services/            quiz, session, plan, scheduler, reset
  db/                  SQLite schema, learning_repo, repo
  data/                CSV loader
  fonts.py             CJK font resolution
assets/fonts/          Noto Sans SC (bundled CJK font)
fig/                   Amino acid structural formula PNGs
data/                  Runtime data directory (auto-created)
```

## Requirements

- Python 3.13+
- Kivy 2.3+
- SQLite3
- Buildozer (Android packaging only)
