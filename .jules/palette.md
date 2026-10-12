# Palette's Journal - UX & Accessibility Learnings

## 2025-02-16 - Accessible Copy-to-Clipboard Micro-Feedback
**Learning:** Icon-only or plain copy buttons in dashboard panels lack feedback for screen reader users and visual clarity for keyboard navigation unless accompanied by explicit ARIA labels (`aria-label`), focus rings (`focus-visible:ring-2`), and clear disabled states prior to resource selection.
**Action:** When adding copy-to-clipboard interactions, ensure the button starts disabled if no active resource is loaded, contains explicit `aria-label` tags, supports keyboard focus indicators, and provides brief visual feedback (e.g. green border + checkmark) for ~2 seconds.
