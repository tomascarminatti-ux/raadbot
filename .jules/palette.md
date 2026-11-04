# Palette's Journal - Critical UX Learnings

## 2026-03-06 - Floating Overlay Placement & Interactive Occlusion
**Learning:** Fixed position debugging panels placed in corners (e.g. `bottom: 20px; right: 20px`) with high `z-index` (such as `1000`) frequently intercept pointer events and obstruct interactive form elements (inputs, submit buttons, action bars) located in standard sidebars. Adding an accessible collapse toggle (`aria-expanded`, `aria-controls`, `aria-label`) paired with keyboard shortcuts (`Escape`) and moving non-critical HUDs to non-blocking viewport positions (e.g., adjacent to navigation sidebars) restores interactive reachability while maintaining observability.
**Action:** Always verify overlay collision boundaries against primary user flows, and ensure floating utility panels provide explicit toggle/minimization controls with ARIA states and keyboard dismissal.
