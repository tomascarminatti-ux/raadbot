## 2024-05-15 - Improving Accessibility and Utility in Dashboard

**Learning:** When visual labels are omitted or styled as decorative headers in industrial dashboards, interactive elements like textareas often lack semantic association. Using `aria-labelledby` to link these headers to inputs maintains the visual design while ensuring screen reader compatibility. Additionally, providing immediate visual feedback (e.g., changing button text/color) for asynchronous actions like clipboard copying significantly reduces user uncertainty.

**Action:** Always verify ARIA associations for inputs that use non-label elements as visual headers. Implement success/feedback states for all "one-click" utility buttons.
