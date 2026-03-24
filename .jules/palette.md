## 2025-05-15 - [Copy to Clipboard Feedback]
**Learning:** Visual feedback for clipboard actions (text change, icon change, color change) significantly improves the perceived responsiveness of the UI. For multi-step selection interfaces, resetting this feedback on new selections is critical for consistency.
**Action:** Always implement a reset mechanism in `selectX` functions when adding ephemeral visual feedback to shared UI components.

## 2025-05-15 - [UI Language Consistency]
**Learning:** The dashboard uses a mix of English and Spanish, but user-facing labels in the content area tend towards Spanish (e.g., "Refinamiento IA").
**Action:** Prefer Spanish for new micro-UX additions in the main content area of `dashboard.html` to maintain local consistency.
