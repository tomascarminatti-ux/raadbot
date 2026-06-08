## 2025-05-15 - Dynamic Log Accessibility
**Learning:** When implementing a custom "terminal" or log view that updates via WebSocket, standard `innerHTML` is both a security risk and unfriendly to screen readers.
**Action:** Use `role="log"` and `aria-live="polite"` on the log container. For rendering, prefer `textContent` for individual log segments or construction via `createElement` to ensure safe and accessible updates.

## 2025-05-15 - Visual Feedback for Collapsible Components
**Learning:** Glassmorphism components benefit significantly from synchronized visual transitions and explicit ARIA state updates.
**Action:** Use CSS transitions (e.g., `transition-all duration-300`) alongside `aria-expanded` and rotational transforms for icons to provide clear interaction feedback for collapsible panels.
