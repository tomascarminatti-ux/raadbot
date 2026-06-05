## 2025-05-15 - Industrial Glassmorphism Log Widget and Accessibility Polish

**Learning:** Dynamic log regions in a "glassmorphism" aesthetic require explicit ARIA roles (role="log", aria-live="polite") on the specific container receiving updates, not just the wrapper, to ensure screen reader compatibility without disrupting the visual blur/transparency effects.

**Action:** Always place ARIA live region attributes on the immediate parent of dynamically appended log entries. Use 'textContent' instead of 'innerHTML' when appending logs from external sources (like WebSockets) to prevent XSS while maintaining the industrial aesthetic.
