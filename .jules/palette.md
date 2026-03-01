## 2025-05-15 - Clipboard and Visual Feedback Best Practices

**Learning:** When testing clipboard functionality with Playwright in headless mode, the browser context must be explicitly granted 'clipboard-write' and 'clipboard-read' permissions. Additionally, providing immediate visual feedback (e.g., color and text changes) for copy actions significantly improves perceived responsiveness and user confidence.

**Action:** Always include permission grants in Playwright scripts for clipboard tests and use temporary state changes (like green background and checkmark icons) for successful user actions.
