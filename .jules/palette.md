# Palette's Journal - Critical Learnings Only

## 2026-03-01 - Scrollable Containers & Interactive Code Access
**Learning:** In text/code-heavy dashboards containing scrollable preformatted elements (like system prompts), keyboard-only and screen reader users are completely locked out of reading off-screen content. Without explicitly setting `tabindex="0"`, these scrollable panels cannot receive focus, preventing keyboard scrolling. Furthermore, they require highly descriptive `aria-label` tags and accompanying copy-to-clipboard utilities with persistent and self-resetting visual cues to achieve full keyboard/screen reader compliance and delightful interactions.
**Action:** Always wrap code/text viewers in focusable, labeled scrollable containers (`tabindex="0"` with `aria-label`) and pair them with visible, feedback-reactive clipboard buttons that clean up their timeouts statefully upon switched view contexts.
