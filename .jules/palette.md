# Palette's Journal - Critical UX Learnings

## 2026-03-06 - Clipboard Action Feedback & Accessible State Transitions
**Learning:** For read-only text containers (like AI prompt displays or token logs), users frequently need to extract raw text without manual selection. Adding a clipboard copy action requires three critical accessibility and UX touchpoints: 1) Initial disabled state until valid content is loaded, preventing empty clipboard writes; 2) Explicit `aria-label` describing the copy target for assistive tech; 3) Multi-modal feedback (both visual icon switch and text confirmation like "Copiado" paired with temporary border/text accent) that automatically reverts after a delay.
**Action:** When creating copy utilities in control panels, always disable before active data selection, include explicit ARIA labeling, and provide clear temporary success state transitions with timeout cleanup.
