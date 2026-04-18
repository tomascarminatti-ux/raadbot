## 2025-05-15 - Collapsible Live Telemetry Drawer
**Learning:** Fixed position elements like floating logs can obstruct interactive parts of the UI. Making them collapsible with smooth transitions improves focus while maintaining observability.
**Action:** Use `aria-expanded` and `role="complementary"` for persistent secondary informational components to ensure screen reader users can manage the state.

## 2025-05-15 - Multi-line Input Keyboard Shortcuts
**Learning:** In dashboards with heavy text input, users expect `Ctrl+Enter` to submit the form without reaching for the mouse.
**Action:** Always attach `keydown` listeners to `textarea` components for `Ctrl+Enter` or `Meta+Enter` submission patterns.
