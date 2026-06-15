## 2025-05-15 - [Collapsible Industrial Overlays]
**Learning:** In busy industrial dashboards with many controls, fixed floating overlays can obstruct critical interactions (like action buttons). Using animatable properties like `max-height` and `opacity` instead of `display: none` provides a smoother transition that preserves the user's spatial context while freeing up screen real estate.
**Action:** Always make secondary monitoring widgets (like logs or activity feeds) collapsible with smooth transitions and clear ARIA state indicators.
