## 2025-07-09 - [Interaction State Reset in Context Switches]
**Learning:** Micro-interaction feedback (like a "Copied" state) with a timeout must be explicitly reset when the user switches context (e.g., selecting a different module) to prevent the feedback state from leaking into the new context and causing UI inconsistency.
**Action:** Always include a cleanup/reset block for active UI timers and stateful classes in the main selection or navigation handlers.

## 2025-07-09 - [Secure Dynamic Rendering & Accessibility]
**Learning:** Refactoring innerHTML to createElement/textContent not only improves security (XSS) but also provides a cleaner path for applying accessibility attributes (aria-label, role) to dynamically generated elements.
**Action:** Use native DOM APIs for all dynamic content insertion to ensure both security and accessible-by-default behavior.
