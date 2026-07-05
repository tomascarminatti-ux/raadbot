## 2025-05-14 - Keyboard Accessibility for Scrollable Regions
**Learning:** In dark-themed, glassmorphism UIs, scrollable containers (like `<pre>` or `<div>`) are often unreachable for keyboard users. Adding `tabindex="0"` makes them focusable, but without explicit Tailwind focus-visible rings (e.g., `focus:ring-2 focus:ring-blue-500/50`), the user won't know which region is active.
**Action:** Always pair `tabindex="0"` with high-contrast focus rings and `aria-label` to ensure scrollable content is accessible and identifiable by screen readers.
