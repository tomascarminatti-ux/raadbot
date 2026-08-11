# Palette's Journal - Critical UX/Accessibility Learnings

## 2025-08-11 - Keyboard Focus Accessibility on Scrollable Containers and Dynamic Nav Controls
**Learning:** Scrollable content containers without `tabindex="0"` cannot be focused by keyboard-only or assistive-technology users, rendering them unable to scroll the content. In addition, dynamic navigation elements rendered purely via JS must explicitly include `focus-visible:ring-2` to support clear focus indicators and `aria-label` for screen reader readability.
**Action:** Ensure any container with `overflow-y-auto` or `overflow-x-auto` has `tabindex="0"` and an `aria-label` for accessibility, and dynamically rendered interactive elements receive keyboard outlines and semantic descriptors.
