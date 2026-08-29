## 2026-08-29 - Fixed log panel positioning & text input contrast in dark theme

**Learning:** Fixed `#live-logs` panel in dark mode can overlap interactive textarea and submit buttons in standard viewports if positioned using `right:20px`. Shifting `right:410px` and adding explicit text styling (`text-slate-200`) ensures clear contrast and unimpeded interactive controls.
**Action:** When working on dark-themed dashboard layouts with fixed overlay panels, ensure proper horizontal offsets and text contrast colors for interactive forms.
