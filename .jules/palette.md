## 2025-05-14 - Accessibility for Scrollable Containers
**Learning:** Screen readers and keyboard-only users cannot easily interact with or read the full content of scrollable elements (like `div` or `pre` with `overflow-y: auto`) unless they are explicitly focusable via `tabindex='0'`.
**Action:** Always add `tabindex="0"` and a descriptive `aria-label` to any container that uses `overflow: auto` or `overflow: scroll` to ensure they are accessible to all users.

## 2025-05-14 - Immediate Visual Feedback for Clipboard Actions
**Learning:** Providing immediate visual feedback (e.g., changing button text to '¡Copiado!') for 'invisible' actions like clipboard operations significantly improves user confidence and perceived responsiveness.
**Action:** Implement a temporary state change (e.g., 2 seconds) for copy buttons to confirm success, and update the `aria-label` to inform screen reader users of the result.
