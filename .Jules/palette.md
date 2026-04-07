## 2025-05-14 - Consistency in Dashboard Layout
**Learning:** The "Live Logs" component in the dashboard used raw inline styles and lacked the glassmorphism aesthetic of the main UI, creating visual dissonance and potentially confusing screen reader users due to its floating nature.
**Action:** When adding supplemental UI widgets, always use the design system's Tailwind classes (like `glass`) and ensure they are collapsible to respect user focus.
