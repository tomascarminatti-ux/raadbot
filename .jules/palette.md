## 2025-05-14 - Keyboard Accessibility for Scrollable Containers
**Learning:** Screen readers and keyboard-only users cannot easily interact with or read the full content of scrollable elements (like `div` or `pre` with `overflow-y: auto`) unless they are explicitly focusable.
**Action:** Always add `tabindex="0"` and a descriptive `aria-label` to scrollable containers to ensure they can be reached via the Tab key and correctly identified by assistive technologies.

## 2025-05-14 - Visual Feedback for Async Clipboard Actions
**Learning:** Providing immediate visual feedback (e.g., changing button text to "¡Copiado!") for "invisible" actions like clipboard operations significantly improves user confidence and perceived responsiveness.
**Action:** Implement temporary text or icon changes on buttons that perform non-visual background tasks to acknowledge success.
