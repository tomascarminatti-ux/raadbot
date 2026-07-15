## 2025-05-15 - Enhancing Prompt Viewer Accessibility and UX

**Learning:** Scrollable containers like `<pre>` or `<div>` with `overflow: auto` are not reachable by keyboard users unless they have `tabindex="0"`. Additionally, providing a descriptive `aria-label` is crucial for screen reader users to understand the context of the focusable area.

**Action:** Always add `tabindex="0"` and a descriptive `aria-label` to scrollable content containers. For copy-to-clipboard buttons, provide immediate visual and textual feedback (e.g., "Copiado" + checkmark) and ensure the state is reset after a timeout or context switch.
