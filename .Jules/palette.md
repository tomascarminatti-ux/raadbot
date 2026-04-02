## 2025-04-02 - [Accessibility & Micro-feedback]
**Learning:** Decorative emojis (🤖, 🚀, etc.) in high-density industrial dashboards create significant screen reader noise if not explicitly hidden. Providing immediate, localized visual feedback (e.g., changing "Copy" to "✅ Copied!") significantly improves perceived responsiveness for utility actions.
**Action:** Always wrap decorative emojis in `<span aria-hidden="true">` and implement transient success states for clipboard operations.
