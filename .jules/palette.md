## 2026-02-25 - Prompt Refinement Keyboard Shortcut & Focus UX
**Learning:** Textareas for multi-line instructions benefit significantly from `Ctrl+Enter` / `Cmd+Enter` keyboard submission shortcuts paired with explicit disabled state handling (disabling before GEM selection & during active requests) to prevent accidental blank/unselected API submissions.
**Action:** When adding text input areas in control panels, always pair `<kbd>` shortcut hints with `keydown` listeners and manage `disabled` state on both the textarea and submission button.
