## 2026-10-06 - Non-obstructive fixed floating panels and prompt copy actions

**Learning:** Fixed position overlay elements (like live log streams) placed in default bottom-right screen coordinates can obstruct primary user interactions in sidebar control layouts (such as chat inputs and submission buttons). Moving floating panels to main content bounds or providing collapsible states preserves layout hierarchy and prevents blocking user focus.

**Action:** Always verify floating/fixed UI overlays against right sidebar boundaries, ensuring interactive form inputs and submission controls remain completely unobscured. Combine copy-to-clipboard buttons with immediate visual state feedback and screen reader ARIA labels.
