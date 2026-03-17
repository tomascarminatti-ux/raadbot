## 2025-05-15 - Interactive Accessibility and Feedback
**Learning:** Combining immediate visual feedback (like "¡Copiado!") with accessibility attributes (ARIA labels, aria-live) and keyboard focus states significantly improves the perceived responsiveness and inclusivity of a dashboard. Small touches like hiding/revealing utility buttons based on context (selection) keeps the UI clean while remaining helpful.
**Action:** Always ensure that new interactive elements have explicit focus styles and ARIA labels, and use `aria-live` for dynamic content updates to support screen reader users.
