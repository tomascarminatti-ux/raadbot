## 2025-05-15 - Clipboard Feedback State Protection
**Learning:** Providing immediate visual feedback for clipboard operations (e.g., changing button text to '¡Copiado!') significantly improves user confidence. However, state restoration logic must be protected against rapid clicks to prevent "freezing" the temporary feedback state as the permanent one.
**Action:** Use a guard clause or check the current state class before initiating a clipboard feedback cycle to ensure `oldText`/`oldIcon` variables don't capture the feedback state itself.
