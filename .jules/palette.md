# Palette's Journal - Critical UX/Accessibility Learnings

## 2025-05-15 - Multi-line inputs and Efficiency
**Learning:** For power-user interfaces like prompt engineering dashboards, multi-line inputs (textareas) feel sluggish if they require a mouse click to submit. Adding `Ctrl+Enter` or `Cmd+Enter` support bridges the gap between typing and execution, significantly improving the perceived speed of the "Refine" loop.
**Action:** Always implement standard submission shortcuts on textareas intended for quick iterative commands.

## 2025-05-15 - Non-blocking Telemetery
**Learning:** Real-time logs are essential for confidence but distracting if they permanently obscure part of the workspace. A collapsible "drawer" pattern with a pulsing status indicator provides enough ambient information (the system is "alive") without competing for the user's focus on the primary task (the prompt content).
**Action:** Use docked, collapsible containers for secondary data streams like logs or background tasks.
