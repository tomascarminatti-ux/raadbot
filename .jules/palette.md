# Palette's Journal - Critical Learnings

## 2025-02-14 - HTML Compliance and Accessible Interaction Feedback
**Learning:** In vanilla HTML dashboards, labels must use the standard `for` attribute rather than JSX's `htmlFor` to correctly associate with inputs for screen readers. Additionally, copy-to-clipboard elements should provide instant visual success feedback (e.g., changing text to "Copiado" and reverting) and support a robust `document.execCommand('copy')` fallback for non-secure (HTTP) or headless browser contexts where `navigator.clipboard` is restricted.
**Action:** Always verify label associations using standard HTML `for` attributes and implement reliable clipboard fallback routines coupled with state-clearing timeouts.
