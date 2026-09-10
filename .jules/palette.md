# Palette's Journal - UX & Accessibility Learnings

## 2025-05-18 - Textarea Keyboard Submission & Dark Theme Contrast
**Learning:** Textarea inputs in dark-themed Tailwind forms require explicit text color definitions (e.g. `text-slate-200`) and keyboard shortcut hints (`Ctrl+Enter` / `Cmd+Enter`) alongside `aria-label` to ensure readable input text and seamless keyboard usability.
**Action:** Always include explicit text colors, keyboard submission handlers (`(e.ctrlKey || e.metaKey) && e.key === 'Enter'`), visible `<kbd>` hints, and accessibility focus indicators (`focus-visible:ring-2`) on multi-line text inputs in dark-themed interfaces.
