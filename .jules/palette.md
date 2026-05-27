## 2024-05-27 - Collapsible Floating Log Window
**Learning:** Fixed-position floating components (like the 'Raadbot Live' logs) can easily obstruct primary dashboard interactions (like the chat refinement). Providing a toggle with a clear visual and ARIA state (`aria-expanded`) is essential for maintaining both visibility and accessibility.
**Action:** Always implement collapse/expand functionality for persistent overlays and ensure state is reflected in ARIA attributes.
