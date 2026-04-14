## 2025-04-14 - Collapsible Telemetry Drawer Pattern
**Learning:** Fixed terminal-style overlays for logs can occlude core interactive areas (like the AI refinement chat) and often lack visual harmony with glassmorphism themes.
**Action:** Use a collapsible drawer with `aria-expanded` and `aria-live="polite"` for secondary telemetry data. This preserves screen real estate while ensuring accessibility for screen reader users through live region announcements.
