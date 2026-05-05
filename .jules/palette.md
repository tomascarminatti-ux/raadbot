## 2025-05-22 - Live Log Accessibility
**Learning:** Live-updating log containers (like the one in this dashboard) are invisible to screen reader users unless explicitly marked with `role="log"` and `aria-live="polite"`. This ensures that new entries are announced without interrupting the current flow.
**Action:** Always apply these attributes to any terminal-style or log-streaming UI component in this ecosystem.
