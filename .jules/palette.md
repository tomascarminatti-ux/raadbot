# Palette's UX Journal

## 2025-05-18 - Scrollable Containers and Focus Accessibility
**Learning:** In highly dense analytical dashboards (like Raadbot), scrollable code panels and logs are frequently used. Without explicit `tabindex="0"` and descriptive `aria-label` attributes, keyboard-only or screen-reader users are completely unable to focus on or scroll through these containers, violating WCAG guidelines.
**Action:** Always include `tabindex="0"` and an appropriate, concise `aria-label` attribute on any container that has overflow-y auto/scroll styling.
