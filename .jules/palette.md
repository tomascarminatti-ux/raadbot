## 2026-03-31 - Keyboard Shortcut UX & Overlay Positioning
**Learning:** Textarea inputs in prompt refinement panels benefit significantly from `Ctrl+Enter` / `Cmd+Enter` shortcuts with visible `<kbd>` visual badges. When handling keydown events for shortcuts, checking button `.disabled` status avoids executing actions prematurely when no module is selected.
**Action:** Always include keyboard shortcut keydown listeners and visual `<kbd>` key hints on multi-line text input forms, ensuring `.disabled` checks prevent accidental triggers.
