## 2025-05-22 - [Safe DOM Updates for Logs]
**Learning:** Using `innerHTML` for real-time log updates from WebSockets is a security risk (DOM XSS).
**Action:** Use `document.createElement` and `textContent` to safely construct log entries while maintaining full styling control via Tailwind CSS classes.

## 2025-05-22 - [ARIA for Collapsible Widgets]
**Learning:** Fixed-position toggle widgets require synchronized visual and semantic state updates (`aria-expanded`, `aria-label`).
**Action:** Ensure toggle icons (▲/▼) are updated alongside `aria-expanded` and descriptive labels to provide a coherent experience for screen reader users.
