## 2025-05-15 - [Dashboard Accessibility & Copy to Clipboard]
**Learning:** Adding `aria-live="polite"` to dynamic chat containers and `aria-label` to dynamically generated buttons significantly improves the screen reader experience without cluttering the UI for sighted users. Providing clear visual feedback for clipboard actions (text change and color shift) reduces user uncertainty.
**Action:** Always include ARIA attributes in dynamic UI updates and ensure visual confirmation for background actions like "Copy to Clipboard".
