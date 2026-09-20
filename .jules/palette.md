# Palette's UX Journal

## 2026-03-20 - Keyboard Shortcuts & Floating Overlays in Dashboard Inputs
**Learning:** Fixed bottom-right overlay panels (such as live websocket loggers) can obscure interactive form controls and input submission areas on standard viewports unless sized compactly and equipped with an accessible minimize/expand toggle button (`#toggle-logs-btn`). Additionally, prompt textareas in dark mode require explicit text contrast classes (`text-slate-200`) and clear shortcut hints (`Ctrl+Enter`) for seamless keyboard workflow.
**Action:** Always ensure floating log panels are collapsible with `aria-expanded` toggle states and do not overlap interactive form inputs; provide explicit input labels, contrast classes, and keyboard submission listeners (`Ctrl+Enter`/`Cmd+Enter`).
