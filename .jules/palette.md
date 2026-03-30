## 2025-05-15 - [Copy to Clipboard Accessibility & Feedback]
**Learning:** Providing immediate visual and ARIA feedback (temporary checkmark icon/text and updating `aria-label`) for clipboard operations like 'Copy System Prompt' significantly improves perceived responsiveness and accessibility. Ensuring the button is hidden until relevant content (a GEM) is selected prevents a confusing 'empty' copy action.
**Action:** Always implement a transient 'success' state for copy buttons and use `aria-hidden` on decorative emojis within those buttons to avoid screen reader noise.

## 2025-05-15 - [Screen Reader Context in Forms]
**Learning:** For floating or specialized inputs (like the prompt refinement textarea), a `.sr-only` label provides essential context for screen readers without altering the visual design.
**Action:** Include visually hidden labels for all interactive elements that lack a visible `<label>`.
