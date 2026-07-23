# Palette's Journal

## 2025-07-23 - High-Density Dashboard Scroll Accessibility
**Learning:** High-density command dashboards and terminals (e.g., system prompts, chat logs, live console outputs) often have overflowing visual elements. Without proper `tabindex="0"` and descriptive `aria-label` attributes, keyboard-only users cannot scroll through long lists, logs, or prompt instructions.
**Action:** Always verify scrollable text and logs panels have `tabindex="0"`, a clear focus indicator, and context-specific ARIA labels.
