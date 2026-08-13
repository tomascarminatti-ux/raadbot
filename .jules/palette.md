# Palette's UX Journal

## 2026-08-13 - Focusable Scroll Containers for WCAG Keyboard Navigation
**Learning:** Scrollable containers with `overflow-y-auto` must explicitly have `tabindex="0"`, a focus ring (`focus-visible:ring-2 focus-visible:ring-blue-500`), and a descriptive `aria-label` to ensure keyboard-only users can focus and scroll them using arrow keys. Without this, users navigating with Tab are locked out of reading long overflow contents.
**Action:** Always add `tabindex="0"`, standard focus rings, and semantic labels to any element containing code, logs, or chat histories that may scroll.

## 2026-08-13 - Headless Browser Copy to Clipboard Fallback
**Learning:** The native `navigator.clipboard.writeText` API can fail or be blocked in headless verification environments (like Playwright), under non-HTTPS origins, or due to iframe sandboxing.
**Action:** Always implement a fallback copying mechanism using a temporary `<textarea>` and `document.execCommand('copy')` to guarantee robust cross-platform copy actions in automated tests and legacy environments.
