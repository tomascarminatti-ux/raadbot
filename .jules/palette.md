## 2025-05-14 - Keyboard Accessibility for Scrollable Containers
**Learning:** Screen readers and keyboard-only users cannot easily interact with or read the full content of scrollable elements (like `div` or `pre` with `overflow-y: auto`) unless they are explicitly focusable.
**Action:** Always add `tabindex="0"` and a descriptive `aria-label` to scrollable containers to ensure they can be reached via the Tab key and correctly identified by assistive technologies.
