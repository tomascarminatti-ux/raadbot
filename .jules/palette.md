## 2025-05-23 - Contextual UI Actions
**Learning:** Utility actions like 'Copy to Clipboard' should be hidden or disabled until their target content is loaded to avoid confusing users with 'Copy' actions on placeholder text. Consistent interface language (e.g., sticking to English for control labels even if content is in another language) maintains professional UI standards.
**Action:** Use CSS `hidden` or `disabled` attributes for buttons that depend on dynamic content, and reveal them only when the state is valid.
