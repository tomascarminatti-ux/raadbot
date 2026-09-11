## 2025-05-18 - Input Focus and ARIA Labeling on Dark Themes
**Learning:** Textarea inputs utilizing Tailwind `outline-none` obscure keyboard focus indicators, making navigation impossible for keyboard-only users unless paired with explicit `focus-visible:ring-2` styles and descriptive `aria-label` attributes.
**Action:** Always verify focus rings (`focus-visible`) and proper ARIA labels when styling custom form inputs with `outline-none`.
