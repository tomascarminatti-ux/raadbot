## 2025-05-22 - [Clipboard Feedback & Accessibility]
**Learning:** Adding visual feedback (text and color changes) for clipboard actions significantly improves the "pleasantness" of the UI. Combining this with standard accessibility (ARIA labels and focus states) ensures the feature is usable by everyone.
**Action:** Always include a visual confirmation state (like '✅ Copiado!') when implementing clipboard or async actions. Use focus-visible rings for all interactive elements to support keyboard-only users.
