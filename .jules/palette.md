## 2025-08-10 - Keyboard Navigation and Focus Styles in Dark Mode Dashboard
**Learning:** In Tailwind-based dark-themed interfaces, standard browser outline rings can have extremely low color contrast or be completely invisible. Explicitly defining custom `focus-visible` ring colors (such as `focus-visible:ring-blue-500` or `focus-visible:ring-green-500`) with `outline-none` ensures interactive and scrollable elements stand out with high contrast, enabling accessible navigation for keyboard-only users.
**Action:** Always pair `tabindex="0"` with high-contrast `focus-visible:ring-2` styling on scrollable boxes and dynamic lists in dark mode interfaces.

## 2025-08-10 - Secure & Bulletproof Copy-to-Clipboard Flow
**Learning:** Native `navigator.clipboard.writeText` might fail inside headless browser tests, insecure origins, or sandboxed environments due to permission constraints. A robust copy action must always fall back to a dynamic `<textarea>` element and `document.execCommand('copy')` to maintain a reliable user experience across all browsing contexts.
**Action:** Implement a transparent fallback clipboard copy utility that degrades gracefully while maintaining UI feedback transition.
