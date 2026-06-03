## 2025-05-24 - Collapsible Overlay for Live Telemetry
**Learning:** Combining the existing `.glass` class with Tailwind utility classes like `bg-black/20` for content areas creates a consistent 'industrial' feel for overlay components. Adding a collapse toggle to persistent overlays (like logs) prevents them from obscuring interactive controls (like the "Refine" button) on smaller viewports.
**Action:** Always provide a collapse/expand mechanism for fixed overlay panels that might overlap with primary CTA buttons.
