# Palette UX Journal

## 2024-08-08 - Keyboard Scroll Accessibility on Read-Only Containers
**Learning:** Any scrollable text block or historical conversation block (like `#prompt-content` or `#chat-history`) that is read-only will block keyboard-only users from scrolling its content if it lacks a `tabindex="0"`. Adding `tabindex="0"`, custom focus rings (`focus-visible:ring-2 focus-visible:ring-blue-500 outline-none`), and clear descriptive `aria-label` tags ensures full compliance with accessibility standards and enables keyboard navigation.
**Action:** Always verify scrollable text containers in any templates have `tabindex="0"`, visual focus outlines, and screen-reader accessible `aria-label` tags.

## 2024-08-08 - Copy-to-Clipboard Fallback for Headless/Insecure Contexts
**Learning:** In headless web browsers, CI environments, or non-secure (HTTP) contexts, the modern asynchronous `navigator.clipboard.writeText` API is disabled. Implementing a robust fallback with a temporarily created `<textarea>` and `document.execCommand('copy')` is essential to prevent JavaScript errors and ensure seamless utility.
**Action:** Always wrap modern Clipboard API calls inside a try/catch block and fall back to the classic DOM-based copy utility.
