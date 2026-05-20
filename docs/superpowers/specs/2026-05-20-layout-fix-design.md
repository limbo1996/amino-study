## Goal
- Fix layout bug where question disappears and options shift up after clicking Next
- Make options positioned lower, reduce button heights by ~1/3

## Root Cause
- `show_answer_area()` / `hide_answer_area()` dynamically change `size_hint_y` on card children
- Kivy BoxLayout re-layout on Android after `size_hint_y` changes causes child positioning bugs
- Nested BoxLayouts (options_box > row1/row2 > buttons) amplify the issue

## Design
- **Never change `size_hint_y` dynamically.** Use fixed proportions, toggle visibility via `opacity` only.
- All card children always present in layout, answer-area widgets are just transparent when hidden.

Card child proportions (sum = 1.0):
| Widget | size_hint_y | Note |
|--------|------------|------|
| question_label | 0.40 | always visible |
| options_box | 0.30 | was 0.5, reduced ~40% |
| image_view | 0.15 | toggle opacity |
| feedback_label | 0.07 | toggle opacity |
| next_button | 0.08 | toggle opacity |

## Changes
- `app/main.py`: remove dynamic `size_hint_y` changes in show/hide functions, use opacity-only toggle
- Set all 5 card children to their final `size_hint_y` at creation, never modify afterward

## Out of Scope
- Font size changes, color changes, non-layout logic
