## 2025-05-15 - [Visual Feedback for Clipboard Actions]
**Learning:** For 'invisible' asynchronous actions like copying to clipboard, providing immediate visual feedback (e.g., changing button text to "¡Copiado!") significantly improves perceived responsiveness and user confidence.
**Action:** Always include success/feedback states for clipboard operations and other silent background tasks.

## 2025-05-15 - [Keyboard Accessibility in Glassmorphism UIs]
**Learning:** Dark-themed glassmorphism interfaces often have poor default focus indicators. Using explicit Tailwind `focus-visible:ring-2` utilities ensures interactive elements are discoverable via keyboard.
**Action:** Proactively add focus-visible rings to all interactive elements, especially in custom-styled dashboard components.
