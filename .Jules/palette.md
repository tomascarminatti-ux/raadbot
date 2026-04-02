## 2026-04-02 - Accessible Feedback for Clipboard Operations
**Learning:** Providing immediate visual and ARIA feedback (temporary icon/text change and updating `aria-label`) for clipboard operations significantly improves perceived responsiveness and accessibility. Decorative emojis should always have `aria-hidden="true"` to prevent screen reader noise.
**Action:** Use a temporary state (e.g., "¡Copiado!") and update the `aria-label` attribute on the copy button, while ensuring decorative elements are hidden from assistive technology.
