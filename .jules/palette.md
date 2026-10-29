## 2026-03-31 - Prompt Copy Button Pattern
**Learning:** System prompt viewers benefit significantly from explicit copy controls with instant visual state feedback (`Copiar` -> `¡Copiado! ✅`) and ARIA labels (`aria-label="Copiar prompt al portapapeles"`), preventing text selection friction and clarifying read-only status.
**Action:** When adding prompt or code viewer panels in control dashboards, integrate an accessible copy button disabled by default until an active module is loaded.
