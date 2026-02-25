## 2025-05-22 - Reusable Copy-to-Clipboard Pattern
**Learning:** Providing immediate visual feedback (text/icon change) for clipboard actions improves perceived responsiveness. Using a global `copyTimeout` with `clearTimeout()` prevents race conditions and visual glitching when users click the button rapidly in succession.
**Action:** Always implement `copyTimeout` management when adding temporary visual feedback states to interactive elements.
