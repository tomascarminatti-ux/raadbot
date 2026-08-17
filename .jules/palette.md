## 2026-08-17 - Robust Copy-to-Clipboard Utility with Fallback
**Learning:** Native `navigator.clipboard.writeText` can throw `NotAllowedError` in headless browser environments or non-HTTPS contexts; attempting a fallback using a temporary fixed `<textarea>` and `document.execCommand('copy')` ensures seamless clipboard operations across all environments.
**Action:** Always wrap `navigator.clipboard.writeText` in a try-catch block and fall back to `document.execCommand('copy')` with visual feedback for copy-to-clipboard interactions.
