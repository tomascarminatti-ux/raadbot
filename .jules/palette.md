# Palette's Journal - UX & Accessibility Learnings

## 2025-05-18 - Accessible Clipboard Copy Feedback for Read-Only Prompts
**Learning:** In prompt management interfaces, providing a 1-click copy action with dynamic ARIA label updates (`aria-label="Prompt copiado al portapapeles"`) and transient visual feedback ("✓ Copiado") improves usability for screen reader and keyboard users without altering read-only prompt integrity.
**Action:** When adding copy buttons to code or prompt viewers, ensure disabled state management when no item is selected, include explicit focus rings (`focus-visible`), and reset transient ARIA and text states after a short delay (e.g. 2000ms).
