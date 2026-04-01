## 2025-05-15 - [Copy to Clipboard & A11y Improvements]
**Learning:** Providing immediate visual and ARIA feedback (temporary checkmark icon/text and updating `aria-label`) for clipboard operations significantly improves perceived responsiveness and accessibility. Additionally, the `sr-only` class is essential for providing context to screen readers for inputs that rely on placeholders.
**Action:** Always include temporary feedback states for clipboard actions and ensure all form inputs have a dedicated (even if hidden) `<label>`.
