## 2025-05-15 - Enhancing Control Panel Accessibility and Feedback

**Learning:** Immediate visual confirmation (like changing button text/icon) for background actions such as "Copy to Clipboard" significantly reduces user uncertainty and improves the perceived responsiveness of the interface. Additionally, utilizing ARIA live regions (`role="log"`, `aria-live="polite"`) is crucial for making real-time, non-interactive status updates (like background logs) accessible to screen reader users without interrupting their flow.

**Action:** Always provide explicit visual feedback for non-visual operations (copy, save, export) and ensure all dynamic content areas have appropriate ARIA roles to keep the interface inclusive.
