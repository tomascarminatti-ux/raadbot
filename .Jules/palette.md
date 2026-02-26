## 2025-05-22 - Visual Feedback for Clipboard Actions
**Learning:** Providing immediate visual feedback (text and color change) after a clipboard action significantly reduces user uncertainty. Using `setTimeout` to reset the button state ensures a smooth micro-interaction.
**Action:** Always include a visual confirmation state when implementing "Copy to Clipboard" buttons, especially in dark-mode dashboards where color shifts are highly visible.

## 2025-05-22 - Keyboard Navigation in Custom Dashboards
**Learning:** Custom Tailwind-based glassmorphism UIs often neglect default focus rings. Adding explicit `focus-visible:ring-2` styles is essential for accessibility and doesn't compromise the aesthetic.
**Action:** Audit all interactive elements (buttons, inputs) in `templates/` for focus states during any UI refinement.
