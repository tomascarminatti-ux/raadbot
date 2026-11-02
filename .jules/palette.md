# Palette's Journal - Critical UX Learnings

## 2026-03-06 - Accessible Clipboard Copy Feedback in Dark Mode Dashboard
**Learning:** In read-only configuration code and prompt viewers within glassmorphic dark interfaces, users frequently need to extract prompts without manual text selection. Pairing an icon (`📋` / `✓`) with explicit text labels (`Copiar` / `Copiado`) and dynamic `aria-label` screen reader announcements ensures both visual and assistive clarity. Maintaining disabled states prior to selecting an active entity prevents blank copies and communicates readiness clearly.
**Action:** When adding copy actions next to read-only badges or content blocks, ensure the button starts disabled until content is populated, toggles ARIA accessibility labels dynamically, provides temporary positive visual feedback (such as green text accent), and resets cleanly using timeouts.
