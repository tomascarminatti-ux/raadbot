# Palette's Journal - UX & Accessibility Learnings

## 2025-05-20 - Accessible Copy-to-Clipboard Button with Dynamic Feedback
**Learning:** Adding interactive copy controls directly to system prompt inspection elements requires robust fallback logic (using standard `document.execCommand('copy')` alongside `navigator.clipboard.writeText`) to support restrictive headless or non-HTTPS contexts without throwing silent JS runtime exceptions. Providing distinct visual confirmation ("✅ Copiado"), explicit `aria-label` attributes, and `focus-visible:ring-2` focus indicators improves clarity for screen readers and keyboard users alike.
**Action:** Always include fallback mechanisms for clipboard interactions and ensure dynamic action feedback is visually distinct and temporary.
