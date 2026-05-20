## Goal
- Require 5 consecutive correct answers per amino acid per day to count toward daily quota
- Wrong answer resets both daily streak and review streak to 0
- Show current progress next to question

## Data Model
- `learning_state` table: add `daily_streak INTEGER DEFAULT 0` and `daily_streak_date TEXT`
- On first question of the day: if `daily_streak_date != today`, reset `daily_streak` to 0

## Logic Flow
```
Answer correct → daily_streak += 1
  ├─ daily_streak == 5:
  │    ├─ increment daily_plan new_done or review_done by 1
  │    ├─ right_streak += 1 (Ebbinghaus)
  │    └─ schedule next_review_at
  └─ daily_streak < 5: continue same amino acid

Answer wrong → daily_streak = 0, right_streak = 0
```

## Session Building
- Filter out amino acids where `daily_streak >= 5` (already completed today)
- Keep generating questions for same amino acid until completed or wrong

## UI
- Question prompt: show `进度：X` (X = current daily_streak, 0~4)
- Smaller font than question text

## DB Schema Migration
- `ALTER TABLE learning_state ADD COLUMN daily_streak INTEGER DEFAULT 0`
- `ALTER TABLE learning_state ADD COLUMN daily_streak_date TEXT`

## Affected Files
- `app/db/schema.py`: migration
- `app/db/learning_repo.py`: new streak logic, modified plan counting
- `app/services/session.py`: session building with streak filter
- `app/services/scheduler.py`: per correct/wrong streak update
- `app/screens/study_screen.py`: progress display helper
- `app/main.py`: progress display in UI

## Out of Scope
- Ebbinghaus interval values unchanged
- Quiz format selection unchanged
