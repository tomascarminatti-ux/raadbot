## 2026-03-05 - Keyboard Focus & Scroll on Fixed/Absolute Panel Containers
**Learning:** Fixed or absolute CSS panels featuring `overflow-y-auto` are inaccessible to keyboard-only and screen reader users unless explicitly configured with `tabindex="0"`, descriptive `aria-label` attributes, and visual focus highlights (such as focus-visible outline rings).
**Action:** Always audit scrollable dashboards for panels with hidden overflow/scrolling, and enforce inclusion of keyboard access and visual focus rings during layout creation.
