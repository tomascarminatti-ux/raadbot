## 2025-05-14 - Collapsible Telemetry & Accessibility
**Learning:** High-contrast, neon-styled fixed overlays can be visually distracting and accessibility-unfriendly. Replacing them with collapsible glassmorphism drawers improves focus. Using manual DOM construction instead of innerHTML for log streams prevents XSS while maintaining styling.
**Action:** Use `textContent` and `createElement` for dynamic log entries. Link dynamic regions to headers via `aria-labelledby` and use `aria-live="polite"` for screen reader updates.
