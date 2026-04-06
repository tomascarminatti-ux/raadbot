## 2025-05-15 - [Accessible Dynamic State Updates]
**Learning:** For buttons that change state visually and textually (e.g., 'Copy' to 'Copied!'), updating the `aria-label` dynamically is essential because assistive technologies might not automatically announce text changes inside the button. Using `aria-live="polite"` on dynamic regions like chat logs ensures immediate but non-intrusive confirmation of actions.
**Action:** Always implement dynamic ARIA labels for state-changing buttons and use `aria-live` for asynchronous UI updates to ensure a smooth experience for screen reader users.

## 2025-05-15 - [Collapsible UI Patterns for Telemetry]
**Learning:** Fixed-position logs or telemetry windows can be intrusive in dense dashboards. Providing a collapsible "drawer" pattern with smooth transitions and clear `aria-expanded` states allows users to focus on the primary task while keeping secondary information accessible.
**Action:** Use collapsible containers for secondary or background processes (like logs) to maximize screen real estate and reduce cognitive load.
