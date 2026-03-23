## 2025-05-14 - Visual Feedback and State Management for Clipboard Interactions
**Learning:** Combining visual feedback (text/icon/color shift) with ARIA label updates for icon-only or small action buttons creates a much more responsive and inclusive experience. Using a global timeout variable to manage successive clicks prevents UI flickering and ensures the feedback duration is consistent.
**Action:** Always implement a 'reset' logic for temporary UI states (like success indicators) that is triggered both by a timeout and by context changes (e.g., selecting a new item).
