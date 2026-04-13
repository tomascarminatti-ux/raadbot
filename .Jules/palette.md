## 2026-04-13 - Collapsible Live Telemetry & Accessibility
**Learning:** For floating UI components like logs or telemetry, a collapsible drawer pattern (using `max-height` transitions) provides a better balance between visibility and workspace management compared to fixed overlays.
**Action:** Use `aria-expanded` and `aria-live="polite"` when implementing such drawers to ensure screen reader users can track state changes and dynamic content. Always mark decorative emojis with `aria-hidden="true"`.
