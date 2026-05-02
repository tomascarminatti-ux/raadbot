## 2025-05-15 - Clipboard Feedback and Log Accessibility
**Learning:** Visual feedback for clipboard actions is critical for user confidence; always provide immediate confirmation (e.g., checkmark, text change) when content is copied. Dynamic logs require explicit ARIA roles (`role="log"`) and live regions (`aria-live="polite"`) to be accessible to screen reader users.
**Action:** Always include success states for copy-to-clipboard buttons and ensure dynamic content containers have appropriate ARIA attributes.
