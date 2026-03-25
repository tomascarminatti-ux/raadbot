## 2026-03-25 - Resetting Transient UI States
**Learning:** When implementing transient UI feedback (like a "Copied!" state on a button), it's crucial to reset this state when the user navigates between items (e.g., selecting a different GEM). Failing to do so can result in misleading feedback where the new item appears as already "Copied" if the previous operation's timeout hasn't cleared.
**Action:** Always include a reset logic for ephemeral states in the selection/navigation handler of the application.
