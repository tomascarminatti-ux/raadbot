## 2025-05-15 - [Accessible Copy Feedback]
**Learning:** For buttons that change state visually (e.g., 'Copy' to 'Copied!'), updating the `aria-label` dynamically is essential because assistive technologies might not automatically announce text changes inside the button. This ensures immediate confirmation of the action for screen reader users.
**Action:** Always pair visual state changes (text/icon) with `aria-label` updates and use `setTimeout` to revert both to ensure the UI remains consistent and accessible.

## 2025-05-15 - [Headless Clipboard Permissions]
**Learning:** When testing features that use the Clipboard API (`navigator.clipboard`) in Playwright's headless mode, browser context permissions for `clipboard-read` and `clipboard-write` must be explicitly granted.
**Action:** Use `browser.new_context(permissions=['clipboard-read', 'clipboard-write'])` in verification scripts.
