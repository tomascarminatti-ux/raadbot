## 2026-04-15 - UI Consistency: Labels and Navigation
**Learning:** For an industrial orchestrator like Raadbot, maintaining English for structural UI components (like "Live Telemetry", "System Prompt") provides a professional, consistent feel even when user-facing agent content is in Spanish.
**Action:** Always prefer English for internal dashboard structural labels to match the "Industrial Orchestrator" theme.

## 2026-04-15 - CSS Flexbox Alignment
**Learning:** The CSS keyword `between` is not a valid value for `justify-content`. It must be `space-between`. Incorrect alignment keywords can silently break layouts in some browsers while appearing partially functional in others.
**Action:** Use `space-between` or Tailwind's `justify-between` class to ensure reliable cross-browser alignment.
