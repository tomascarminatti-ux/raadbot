# Palette's Journal - UX & Accessibility

## 2024-08-06 - Initial setup
**Learning:** Establishing the UX guidelines journal.
**Action:** Document future learnings about dashboard.html design and accessibility as discovered.

## 2024-08-06 - Clipboard Copy Fallback Compatibility
**Learning:** Modern browser Clipboard APIs (`navigator.clipboard.writeText`) are secure-context only and require specific permissions in some clients (e.g. headless browsers or sandbox testing environments), which often cause them to throw unexpected runtime errors instead of seamlessly falling back.
**Action:** Always wrap `navigator.clipboard.writeText` in a nested try/catch block. If it throws, immediately fall back to the programmatic Selection + `document.execCommand('copy')` routine to guarantee cross-client reliability and persistent visual feedback.
