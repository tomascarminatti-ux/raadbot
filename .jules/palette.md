## 2026-03-30 - Clipboard API Fallback in Dashboard Controls
**Learning:** Native `navigator.clipboard.writeText` may fail or be restricted in non-HTTPS, iframe, or headless testing environments. Providing a `document.execCommand('copy')` fallback with explicit ARIA label and transient visual state feedback ("✅ Copiado") ensures seamless user interaction and accessibility across all browser environments.
**Action:** Always wrap clipboard copying in a fallback block and toggle visual feedback classes and ARIA states transiently.
