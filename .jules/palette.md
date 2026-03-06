## 2025-05-15 - [Copy to Clipboard and ARIA labels]
**Learning:** Adding immediate visual feedback (text change + icon swap) significantly improves the perceived responsiveness of "Copy to Clipboard" actions. Additionally, using `aria-label` on dynamic lists (like GEM selection) ensures screen readers provide context for buttons that might otherwise only contain a name.
**Action:** Always implement a 2-second feedback state for clipboard actions and ensure dynamic buttons have descriptive `aria-label` attributes.
