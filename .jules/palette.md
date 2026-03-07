## 2025-03-05 - Add Copy to Clipboard and Improve Accessibility

**Learning:** Users often need to copy system prompts for external use or auditing. A hidden copy button that reveals itself only when an entity (GEM) is selected reduces UI clutter while maintaining functionality. Using temporary visual feedback (checkmark and text change) provides clear success confirmation without persistent notifications.

**Action:** Implement "Copy to Clipboard" with temporary feedback states for large text blocks. Ensure sidebar navigation items have explicit `aria-label` and `focus-visible` indicators for better screen reader and keyboard support.
