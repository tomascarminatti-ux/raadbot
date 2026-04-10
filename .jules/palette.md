# Palette's Journal - Critical UX/Accessibility Learnings

## 2025-05-14 - [A11y & Feedback: Copy to Clipboard]
**Learning:** For buttons that change state visually (e.g., 'Copy' to 'Copied!'), updating the `aria-label` dynamically is essential because assistive technologies might not automatically announce text changes inside the button. This ensures immediate confirmation of the action for screen reader users. Additionally, using `focus-visible:ring-2 focus-visible:ring-blue-500 outline-none` for keyboard navigation focus states on interactive elements in the Tailwind-based dashboard ensures visibility for keyboard-only users without affecting mouse users.
**Action:** Always pair visual state changes with ARIA attribute updates for dynamic feedback. Ensure all interactive elements have visible focus states using `focus-visible`.
