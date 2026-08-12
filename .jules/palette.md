# Palette's Journal - Critical UX/Accessibility Learnings

## 2026-08-12 - [Dark Theme Text Contrast & Copy Utilities]
**Learning:** In highly customized dark mode developer control panels, form elements like textareas often default to browser user-agent text colors (e.g. black text on a dark gray `#1e293b` background), yielding extremely poor text contrast ratio. Explicitly setting `text-slate-200` ensures WCAG AA/AAA level readability. Furthermore, read-only code/prompt blocks are much more usable when paired with a "Copy to Clipboard" button utilizing a headless-safe element-fallback pattern.
**Action:** Always define explicit text colors on Tailwind form controls in dark themes, provide focus rings for keyboard navigation, and add direct Copy controls with fallback copy procedures to optimize headless browser testing and developer workflows.
