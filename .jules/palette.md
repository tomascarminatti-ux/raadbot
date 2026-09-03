## 2026-02-25 - Copy to Clipboard Fallback & ARIA State Management
**Learning:** In headless browser environments or insecure HTTP contexts, `navigator.clipboard.writeText` fails or throws DOM exceptions. Providing an automated fallback (`document.execCommand('copy')`) and dynamically updating `aria-label` alongside visual button state ensures seamless accessibility and feedback across all browser execution environments.
**Action:** Always wrap clipboard API calls with a try-catch fallback and update screen reader ARIA labels alongside DOM text content updates.
