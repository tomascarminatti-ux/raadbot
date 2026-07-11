## 2025-07-11 - [UX] Interactive Copy-to-Clipboard with State Management
**Learning:** Adding interactive elements like a "Copy" button in a multi-item navigation context (like a list of GEMs) requires explicit state management (e.g., clearing timeouts) to prevent visual state "leakage" between different items.
**Action:** Always include a reset mechanism in the item-selection logic for any transient UI states (copy feedback, loading indicators, expanded sections).

## 2025-07-11 - [A11y] Enhancing Keyboard Nav for Scrollable Content
**Learning:** Large scrollable blocks of text (like System Prompts) are often unreachable for keyboard-only users if they don't have a focusable ancestor or the element itself isn't focusable.
**Action:** Apply `tabindex="0"` and descriptive `aria-label` to large scrollable containers to ensure screen reader and keyboard accessibility.
