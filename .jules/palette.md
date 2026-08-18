# Palette UX Journal

## 2025-08-18 - Copy-to-Clipboard Fallback & Dark Theme Input Contrast
**Learning:** Modern browser security contexts or headless test environments can throw permissions errors on `navigator.clipboard.writeText`. Supplying a fallback mechanism using `document.execCommand('copy')` on a temporary off-screen textarea ensures universal copy support. Additionally, dark Tailwind textareas without explicit text color classes (like `text-slate-200`) can fall back to user-agent dark text default styling, causing illegible dark-on-dark contrast.
**Action:** Always complement `navigator.clipboard.writeText` with an `execCommand('copy')` DOM fallback, and explicitly specify light text colors (`text-slate-200`) on dark-themed input controls.
