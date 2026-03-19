## 2025-05-14 - Visual & Accessibility Feedback for Copy Interaction
**Learning:** Combining immediate visual feedback (text/color shift) with dynamic `aria-label` updates and `aria-live` regions creates a significantly more responsive and inclusive experience for clipboard interactions. Visual-only cues (like icons) are insufficient for screen reader users who need state confirmation.
**Action:** Always pair visual state changes with equivalent ARIA attribute updates (e.g., `aria-label`, `aria-expanded`, or `aria-checked`) to ensure accessibility parity.
