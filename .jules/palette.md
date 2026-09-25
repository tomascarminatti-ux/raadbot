## 2026-02-26 - Accessible Copy Action Feedback & ARIA States
**Learning:** When adding interactive actions like "Copy to Clipboard" for code or prompt blocks, dynamic visual feedback ("Copiar" -> "✅ Copiado") must be paired with dynamic `aria-label` updates ("Prompt copiado al portapapeles") and focus styles (`focus-visible:ring-2`) to ensure both visual users and screen reader users receive immediate confirmation of the action.
**Action:** Always maintain dedicated text/icon spans and update accessible ARIA labels alongside visual state timeouts in UI action buttons.
