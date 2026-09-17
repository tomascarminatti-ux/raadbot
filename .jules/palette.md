# Palette's Journal - UX & Accessibility Learnings

## 2026-03-31 - Clipboard Copy Micro-Interactions in Prompt Viewers
**Learning:** In LLM dashboard tools where prompt content is displayed in read-only viewers, providing an immediate copy-to-clipboard button with visual state changes (icon + label feedback) significantly improves user workflow efficiency when inspecting or testing system prompts locally.
**Action:** Always include explicit `aria-label`, disabled state until content is loaded, and temporary visual feedback ("Copiado! ✓") for clipboard actions.
