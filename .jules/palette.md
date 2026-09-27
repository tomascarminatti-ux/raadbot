## 2026-02-27 - Keyboard Shortcut Support for Textarea Submission
**Learning:** In dark-themed textareas with multi-line inputs, users naturally expect `Ctrl+Enter` / `Cmd+Enter` shortcuts to submit prompt refinements without reaching for the mouse, accompanied by explicit `<kbd>` shortcut indicators and explicit foreground text color (`text-slate-200`) for contrast.
**Action:** When adding textareas for chat or prompt refinements, always pair a `keydown` listener for `(e.ctrlKey || e.metaKey) && e.key === 'Enter'` with `<kbd>` shortcut badges and dark-mode contrast styling.
