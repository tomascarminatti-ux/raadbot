# Palette's Journal - Raadbot UX

## 2025-05-14 - Keyboard Accessible Scroll Areas
**Learning:** Large scrollable areas like code blocks or logs (e.g., `#prompt-content`) are not keyboard-accessible by default. Screen reader users and keyboard-only users cannot scroll these areas unless they have a `tabindex`.
**Action:** Always add `tabindex="0"` and a descriptive `aria-label` to scrollable containers that don't have interactive children.

## 2025-05-14 - Copy to Clipboard Feedback
**Learning:** Users need immediate visual confirmation when copying text to the clipboard. Replacing the button text/icon temporarily with a success state (e.g., "Copiado") provides better feedback than just a toast or no feedback at all.
**Action:** Implement a 2-second success state for copy buttons, changing text to "Copiado" and adjusting colors.
