# Palette's Journal - Critical UX/Accessibility Learnings

## 2025-05-14 - Accessible Scrollable Containers
**Learning:** Scrollable containers (like `<pre>` or `<div>` with `overflow: auto`) are not keyboard-accessible by default in many browsers. Users who rely on keyboards cannot focus them to scroll through long content.
**Action:** Always add `tabindex="0"` and a descriptive `aria-label` to scrollable regions to ensure they can be focused and scrolled using arrow keys.
