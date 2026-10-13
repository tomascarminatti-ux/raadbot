## 2026-02-25 - Prompt Refinement Keyboard Shortcut & Accessibility
**Learning:** Adding keyboard shortcuts like Ctrl+Enter / Cmd+Enter on textareas in control panels significantly speeds up prompt iteration while keeping focus intact, and pairing them with explicit `aria-label` and `placeholder` hints ensures both keyboard power-users and screen reader users are informed.
**Action:** When adding textareas for quick AI/prompt refinements, always include `aria-label`, visible keyboard shortcut hints, and a keydown listener for `Ctrl+Enter` / `Cmd+Enter`.
