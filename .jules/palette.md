## 2026-03-31 - Explicit Clipboard Action Feedback
**Learning:** In dark-themed code or prompt inspection panels, providing explicit clipboard action feedback ("✓ Copiado") with stateful color changes (green tint and border highlight) directly on the copy button gives immediate confirmation to users without disrupting layout or requiring modal popups/toast banners.
**Action:** Always couple clipboard copy buttons with dynamic text/icon updates and dynamic `aria-label` updates to ensure screen readers and visual users receive instant feedback.
