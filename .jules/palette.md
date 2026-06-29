# Palette's Journal - UX/Accessibility Learnings

## 2025-02-12 - Copy-to-clipboard Visual Feedback
**Learning:** Providing immediate visual feedback (e.g., changing button text to '¡Copiado!') for 'invisible' actions like clipboard operations significantly improves user confidence and perceived responsiveness. Managing feedback state using a global timeout variable prevents race conditions.
**Action:** Always include a success state for clipboard actions and update ARIA labels to reflect the current state.
