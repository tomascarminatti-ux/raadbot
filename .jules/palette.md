# Palette UX Journal

## 2026-08-30 - Clipboard Copy Fallback and Visual Confirmation in Dark Dashboards
**Learning:** In headless or restricted browser environments (or HTTP contexts), the `navigator.clipboard` API can throw permission errors. Providing a hidden `<textarea>` fallback using `document.execCommand('copy')` ensures seamless copy functionality for system prompts across all environments. Furthermore, dynamic state feedback (`📋 Copiar` -> `✅ Copiado`) paired with updated `aria-label` screen reader announcements gives immediate clarity to users.
**Action:** Always pair `navigator.clipboard` calls with a `document.execCommand('copy')` fallback and temporary visual/aria feedback when implementing copy-to-clipboard actions in web applications.
