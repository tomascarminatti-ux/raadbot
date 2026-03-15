## 2025-05-14 - Interactive Dashboard Feedback & Accessibility
**Learning:** Adding visual feedback to clipboard actions (text change + color shift) significantly improves the perceived responsiveness of the UI. Combining this with ARIA labels for icon-only buttons ensures a delightful experience for all users, including those using assistive technologies.
**Action:** Always include temporary visual state changes (e.g., checkmarks, color changes) for background actions like "Copy" and ensure all navigation/action buttons have explicit `aria-label` attributes.
