## 2025-05-18 - Copy-to-Clipboard Feedback Pattern for Read-Only Prompt Viewers
**Learning:** For read-only prompt or code view blocks in complex agent control panels, providing an inline copy button with direct text/color state transition ("📋 Copiar" -> "✓ ¡Copiado!") gives immediate, clear confirmation without requiring disruptive toast notifications.
**Action:** Use inline copy buttons with explicit ARIA labels (`aria-label="Copiar System Prompt al portapapeles"`), keyboard focus ring styling (`focus-visible:ring-2`), and non-disabled states upon active item selection.
