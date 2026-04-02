## 2025-05-14 - Accessible Clipboard Feedback Pattern
**Learning:** Providing immediate visual (icon/text change) and ARIA (`aria-label` update) feedback for clipboard operations improves perceived responsiveness and screen reader compatibility. Using a global timeout that is cleared on new selections prevents UI state leaks.
**Action:** Always implement a `reset` function for transient UI states like "Copied!" and update `aria-label` dynamically to announce success to assistive technologies.
