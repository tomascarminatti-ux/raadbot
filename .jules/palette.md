## 2026-02-26 - Accessible Copy Button with Visual Feedback
**Learning:** Adding a copy-to-clipboard action to system prompt containers significantly improves developer workflow when inspecting GEM instructions. Providing instant visual feedback ("✅ Copiado") for 2 seconds alongside ARIA labels and keyboard focus ring indicators ensures a seamless and accessible user experience.
**Action:** When adding clipboard interactions, manage button disabled state until active content is loaded, use `aria-label` for screen reader clarity, and reset state via `setTimeout`.
