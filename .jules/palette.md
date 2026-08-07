# Palette Journal

## 2026-03-05 - Clipboard Permission Failures and Interactive Control UX
**Learning:** Native `navigator.clipboard.writeText` can easily fail in headless, secure, or iframe environments due to permission constraints. A fallback method using a temporarily appended `<textarea>` and `document.execCommand('copy')` remains necessary to guarantee smooth clipboard operations across all client environments.
**Action:** Always wrap clipboard code in safe try/catch structures and design robust programmatic fallbacks when implementing Copy utilities.
