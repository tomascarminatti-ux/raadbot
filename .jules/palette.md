# Palette's Journal - Critical UX & Accessibility Learnings

## 2026-03-30 - System Prompt Copy Feedback
**Learning:** Adding a copy-to-clipboard button with visual state changes (`✓ Copiado`) in a read-only code/prompt viewer provides immediate confirmation and saves manual selection effort.
**Action:** Always include temporary state indicators (e.g. 2s reset), `aria-label`, and `focus-visible` styling for action feedback on clipboard buttons.
