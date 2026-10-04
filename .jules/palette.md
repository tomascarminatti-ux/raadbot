# Palette Journal - Raadbot UX Learnings

## 2025-05-18 - Copy-to-Clipboard Action for Read-only Prompts
**Learning:** In dashboard interfaces displaying long read-only prompts or code blocks, users frequently need to copy full contents. Pairing the read-only indicator badge with a dedicated Copy button (`#copy-btn`) using temporary visual state feedback (`Copiar 📋` -> `Copiado ✅` for 2s) provides instant confirmation without requiring modal overlays.
**Action:** When implementing copy-to-clipboard buttons, manage `aria-label`, disabled states prior to content loading, and use `setTimeout` to restore initial state after 2 seconds.
