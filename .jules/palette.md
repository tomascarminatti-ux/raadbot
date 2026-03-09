## 2025-03-09 - Critical Risk: Test Asset Isolation
**Learning:** verification scripts (like Playwright) that generate 'dummy' assets must NEVER use existing project directories (e.g., `prompts/`) as they might overwrite critical production data.
**Action:** Always use dedicated temporary directories for test files or verify if a file exists before creating a 'dummy' version during verification.

## 2025-03-09 - Accessible Feedback for Copy Operations
**Learning:** Users expect immediate visual confirmation for non-visible background actions like "Copy to Clipboard". Combining text changes ("Copiar" -> "¡Copiado!") with icon and border color transitions provides a clear success state.
**Action:** Implement multi-modal feedback (text + icon + color) for transient UI actions.
