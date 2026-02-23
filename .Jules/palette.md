## 2025-05-22 - [Accessibility & Keyboard Interaction in Dashboard]
**Learning:** For tool-heavy dashboards like Raadbot, keyboard shortcuts (Ctrl+Enter) and clear visual feedback for copy actions (icon + text change) significantly improve the perceived speed and utility of the interface. Focus-visible rings are essential for navigating the complex sidebar/content layout without a mouse.
**Action:** Always implement `focus-visible:ring-2` on interactive elements and provide temporary success states (e.g., "¡Copiado!") for background actions like clipboard operations.
