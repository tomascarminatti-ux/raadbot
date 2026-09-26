# Palette's Journal - Critical UX & Accessibility Learnings

## 2026-02-26 - Accessible Copy Button & Scroll Region in Dashboard Viewer
**Learning:** Adding a copy-to-clipboard action on read-only prompt containers requires explicit visual feedback ("¡Copiado!"), accessible focus outlines (`focus-visible:ring-2`), disabled state handling when no GEM is selected, and keyboard scrollability (`tabindex="0"`) with `aria-label` so screen readers and keyboard users can easily inspect long prompt text.
**Action:** Always complement read-only code/prompt blocks with a copy button and accessible scroll region (`tabindex="0"`) on dark glassmorphism interfaces.
