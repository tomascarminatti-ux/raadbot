## 2025-05-14 - [Accessible Chat & Robust Clipboard]
**Learning:** Using `aria-live="polite"` on chat history containers ensures that asynchronous AI responses are announced to screen readers without interrupting the user. Providing a fallback for `navigator.clipboard` using a hidden `textarea` is essential for robustness in non-secure or legacy environments.
**Action:** Always include `aria-live` on dynamic response areas and implement robust clipboard fallbacks for utility features.
