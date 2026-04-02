# Palette's Journal - Critical UX/Accessibility Learnings

## 2024-05-15 - Improving Accessibility and Utility in Dashboard
**Learning:** Icon-only buttons and purely visual state updates (like changing colors or text) aren't enough for screen reader users. Adding `aria-label` and `aria-live` regions ensures all users are informed of system states and actions.
**Action:** Always provide `aria-label` for icon buttons and use `aria-live` for dynamic content like chat histories or log streams.
