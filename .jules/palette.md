## 2025-05-22 - [Optimized Live Logs Accessibility]
**Learning:** For dynamic log regions in Tailwind/glassmorphism widgets, place `aria-live="polite"` and `role="log"` directly on the scrolling child container where content is appended rather than the static parent wrapper. This prevents screen readers from re-announcing static UI elements like headers on every update.
**Action:** Always identify the specific content-delivery container for ARIA live regions in dashboard widgets.
