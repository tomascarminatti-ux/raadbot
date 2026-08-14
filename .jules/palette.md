# Palette's Journal - Critical Learnings

## 2026-03-04 - [Dashboard Prompt Viewer Copy Utility]
**Learning:** Adding a native fallback copy-to-clipboard mechanism prevents standard browser restriction issues (especially in non-secure or headless environments). Ensuring a clear visual feedback state (e.g. changing text/color to "✅ Copiado") and proper disabled states makes the tool intuitive and accessible to keyboard/screen reader users.
**Action:** Always provide robust disabled-to-enabled state transitions, ARIA attributes, and explicit visual/haptic-like feedback on clipboard copy tasks.
