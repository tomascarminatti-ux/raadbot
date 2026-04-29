## 2025-05-14 - Accessible Live Logs and UI Feedback
**Learning:** Real-time updates (like WebSocket logs) can be disorienting for screen reader users if not properly announced using `role="log"` and `aria-live="polite"`. Additionally, visual feedback for actions like "Copy to Clipboard" needs both an icon change and a text change to be truly intuitive.
**Action:** Always include ARIA live regions for log containers and ensure all "quick actions" provide clear, multi-modal feedback (visual + text).
