## 2025-05-24 - Live Logs Component Refactor
**Learning:** Refactoring legacy hardcoded styles into a unified design system (Tailwind + .glass utility) not only improves visual consistency but also allows for easy implementation of complex interactions like collapse/expand toggles. Adding `aria-expanded` and `aria-live="polite"` ensures these dynamic UI elements remain accessible to screen reader users.
**Action:** Always prefer utility classes over inline styles to keep components flexible and accessible.
