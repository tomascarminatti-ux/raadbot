## 2025-05-14 - Robust Clipboard Feedback
**Learning:** Combining visual feedback (text/color shift) with ARIA labels for buttons creates a more responsive experience. When implementing temporary UI states (like "Copied!"), it's crucial to manage a global timeout variable to prevent flickering or inconsistent states during rapid, successive interactions.
**Action:** Always use `clearTimeout` when resetting temporary UI states triggered by user actions to ensure a clean transition back to the default state.
