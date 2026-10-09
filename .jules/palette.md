# Palette Journal

## 2025-05-18 - Input Field Accessibility and Keyboard Navigation
**Learning:** Textarea inputs in chat-like panels need explicit `aria-label` attributes for screen reader accessibility, and disabling inputs prior to selecting an active context (e.g. active GEM module) prevents user confusion or orphaned submissions. Providing standard `Ctrl+Enter` / `Cmd+Enter` keyboard shortcuts with visual `<kbd>` hints significantly improves power-user UX without clogging the visual layout.
**Action:** Always include ARIA labels, initial disabled/active state management tied to context selection, and standard keyboard submission shortcuts with visual feedback on input areas in control dashboards.
