## 2025-05-14 - Visual Feedback & Accessibility Synergy
**Learning:** Combining dynamic visual feedback (color/text shifts) with updated ARIA labels creates a superior experience for both sighted and screen-reader users. Resetting these states explicitly on context changes (like switching items in a list) is crucial to avoid "stale" feedback.
**Action:** Always include state resets in UI handlers that change the active context, and ensure ARIA labels are updated alongside visual changes.
