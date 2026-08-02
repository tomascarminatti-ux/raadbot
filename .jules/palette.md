# Palette's Journal - Critical UX and Accessibility Learnings

## 2026-03-05 - [Dashboard Accessibility & Copy Utilities]
**Learning:** For interactive dashboards containing core components like dynamic prompts, having accessible keyboard interactions, explicit focus indicators, and custom Copy-to-Clipboard buttons with clear visual and screen-reader feedback makes developer interfaces vastly more pleasant. Also, a fallback utility is necessary for `navigator.clipboard` because browser security constraints or headless browser testing sessions often disable standard clipboard writing.
**Action:** Always provide key navigation rings, tabindex for scrollable panels, and fallback Copy-to-Clipboard strategies in interactive templates.
