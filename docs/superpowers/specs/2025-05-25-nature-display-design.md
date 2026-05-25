# Spec: Display Amino Acid "性质" (Nature/Property) in Quiz UI

**Date:** 2025-05-25
**Status:** Approved

## Goal

Add the amino acid "性质" (chemical nature: charge, polarity) from the CSV to the quiz question display, shown on a second line below the amino acid name with distinct font sizes.

## Current State

- CSV `deepseek_csv_20260513_f1933c.csv` has a `性质` column with values like "非极性脂肪族", "碱性（带正电）", etc.
- The application completely ignores this column:
  - `app/data/loader.py` reads `"分子式"` (which does not exist) instead of `"性质"`
  - DB `amino_acids.formula` is always empty
  - No property text appears anywhere in the UI
- Current quiz display: single line `name_cn (name_en)  进度：streak` at `font_size=64`

## Target Display

Two-line layout in `question_label`:

```
丙氨酸 (Alanine)  进度：3          ← font_size=64 (unchanged)
非极性脂肪族                        ← font_size=28 (smaller by 3 levels)
```

- Progress counter stays on the first line
- Nature text displayed without prefix label
- If `nature` is empty, second line is blank

## Files Changed

| File | Change |
|------|--------|
| `app/data/loader.py` | Add `"性质"` to `REQUIRED_FIELDS`; extract `nature` from row |
| `app/db/schema.py` | New `migrate_add_nature()`: `ALTER TABLE amino_acids ADD COLUMN nature TEXT NOT NULL DEFAULT ''` |
| `app/bootstrap.py` | Call `migrate_add_nature(db_path)` after existing migration |
| `app/services/session.py` | Add `nature` to `_fetch_items_by_ids()` SELECT and question dict |
| `app/screens/study_screen.py` | `build_question_prompt()` returns Kivy markup with `[size=64]...[size=28]...` tags |
| `app/main.py` | Set `question_label.markup = True` |

## Implementation

### Data Layer

1. **`app/data/loader.py`**: Add `"性质"` to `REQUIRED_FIELDS` tuple. Extract `row.get("性质", "").strip()` as `nature`. Return it in the record dict alongside existing fields. Update embedded fallback data to include `"nature": ""`.

2. **`app/db/schema.py`**: Add `migrate_add_nature(db_path)`. Pattern matches `migrate_add_daily_streak()` — try `ALTER TABLE amino_acids ADD COLUMN nature TEXT NOT NULL DEFAULT ''`, catch `sqlite3.OperationalError` for idempotency.

3. **`app/bootstrap.py`**: Call `migrate_add_nature(db_path)` in `bootstrap_storage()` after `migrate_add_daily_streak(db_path)`.

### Service Layer

4. **`app/services/session.py`**: In `_fetch_items_by_ids()`, add `nature` to the SELECT list. Include `nature` in each returned dict.

### UI Layer

5. **`app/screens/study_screen.py`**: Modify `build_question_prompt()`:
   ```python
   def build_question_prompt(question: dict) -> str:
       name_cn = question.get("name_cn", "").replace("[", "&bl;").replace("]", "&br;")
       name_en = question.get("name_en", "").replace("[", "&bl;").replace("]", "&br;")
       nature = question.get("nature", "").replace("[", "&bl;").replace("]", "&br;")
       streak = question.get("daily_streak", 0)
       return (
           f"[size=64]{name_cn} ({name_en})  进度：{streak}[/size]\n"
           f"[size=28]{nature}[/size]"
       )
   ```

6. **`app/main.py`**: Set `question_label.markup = True` on the existing `Label` widget.

### Edge Cases

- **Empty nature**: Second line renders as empty (no visible artifacts)
- **Kivy markup escaping**: `[` and `]` in amino acid names/properties escaped to `&bl;` / `&br;` before embedding in markup
- **Migration idempotency**: `migrate_add_nature()` catches `OperationalError`; safe to call on every app start
- **No `size_hint_y` changes**: The single Label widget with markup preserves the existing layout constraints, avoiding the known Android crash

## Excluded

- No changes to `quiz.py` (quiz service) — nature is display-only, not used in question logic
- No change to `learning_repo.py` — nature is not needed for learning state queries
- No change to `insert_amino_acids()` — the loader already passes all fields; the repo INSERT will include `nature` automatically once the column exists

## Testing

- Unit test for `build_question_prompt()` with and without nature text
- Integration test: CSV → DB → question dict → display text
- Verify migration idempotency
- Verify markup escaping for names containing brackets (none currently do, but guard added)
