## 2025-05-22 - [Accessibility & Keyboard Interaction in Dashboard]
**Learning:** For tool-heavy dashboards like Raadbot, keyboard shortcuts (Ctrl+Enter) and clear visual feedback for copy actions (icon + text change) significantly improve the perceived speed and utility of the interface. Focus-visible rings are essential for navigating the complex sidebar/content layout without a mouse.
**Action:** Always implement `focus-visible:ring-2` on interactive elements and provide temporary success states (e.g., "¡Copiado!") for background actions like clipboard operations.

## 2025-05-22 - [Clipboard API and Headless Verification]
**Learning:** `navigator.clipboard` requires a secure context and proper permissions in headless environments. Using `async/await` with `try/catch` makes the feature more robust and allows for better error handling/fallbacks.
**Action:** Always wrap clipboard operations in `async` functions with proper error handling.
