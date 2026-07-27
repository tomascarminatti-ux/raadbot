# Palette UX/Accessibility Journal - Critical Learnings Only

## 2026-02-25 - Interactive Feedback Patterns and Keyboard Access for Scrollable Elements
**Learning:** For a more accessible and intuitive experience in rich, technical dashboards:
1. Interactive scrollable elements like `<pre>` code viewers, terminal logs, or chat histories must have `tabindex="0"` and an explicit descriptive `aria-label` to ensure screen-reader and keyboard-only navigation.
2. In headless Playwright testing environments, testing the modern `navigator.clipboard` API requires granting explicit permission to the browser context: `context.grant_permissions(['clipboard-read', 'clipboard-write'])`.
3. High-use textareas inside AI interactive dashboards benefit from standard `Ctrl + Enter` shortcuts, which should be explicitly hinted in placeholders to improve user discoverability.
**Action:** Always include tab indices and descriptive labels for custom scrollable blocks, explicitly grant context permissions in Playwright tests targeting the clipboard, and provide keyboard-shortcut hints in inputs.
