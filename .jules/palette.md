## 2025-05-14 - [Dynamic ARIA Labels for State Changes]
**Learning:** For buttons that change state visually (e.g., "Copy" to "Copied!"), updating the `aria-label` dynamically is essential. Assistive technologies may not automatically announce the text change inside the button unless it's an ARIA live region. Updating the `aria-label` ensures the user receives immediate confirmation of the action.
**Action:** Always pair visual text changes with corresponding `aria-label` updates on interactive elements to maintain accessibility.
