## 2025-05-14 - Interactive Dashboard Accessibility
**Learning:** In dashboards with long scrollable areas (like prompt logs or chat histories), adding `tabindex="0"` and an `aria-label` to the container is critical for keyboard-only users to be able to focus and scroll through the content.
**Action:** Always ensure large scrollable areas have `tabindex="0"` and a descriptive `aria-label` in the appropriate language.

## 2025-05-14 - Clipboard UX Feedback
**Learning:** Providing immediate visual feedback for clipboard operations (e.g., changing button text to '¡Copiado!' and icon to '✅' for 2 seconds) significantly improves user confidence and perceived responsiveness.
**Action:** Implement transient success states for clipboard-related actions to confirm the operation succeeded without needing a separate toast notification.
