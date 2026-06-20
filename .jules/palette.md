## 2025-05-14 - Clipboard Feedback Pattern
**Learning:** Providing immediate visual feedback (e.g., "¡Copiado!") for async clipboard actions significantly improves perceived responsiveness and user confidence. In a dark-themed UI, using a high-contrast but soft color like `text-green-400` works well for success states.

**Action:** Always pair clipboard operations with a temporary visual state change or notification.

## 2025-05-14 - Keyboard Navigation Visibility
**Learning:** Default browser focus rings are often suppressed in modern Tailwind-based designs, making keyboard navigation nearly impossible for users who rely on it. Using `focus-visible:ring-2` allows for high-visibility focus states only when needed (keyboard), preserving the aesthetic for mouse users.

**Action:** Ensure all interactive elements (buttons, inputs, links) have explicit `focus-visible` ring styles.
