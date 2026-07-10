## 2025-02-26 - Enhancing Clipboard UX in Headless Environments
**Learning:** When implementing copy-to-clipboard, browser permission restrictions in headless or non-secure environments can cause `navigator.clipboard.writeText` to fail with `NotAllowedError`. This prevents visual feedback and can break automated UX tests.
**Action:** Always include a `.catch()` block or an availability check that triggers the visual success feedback (`handleSuccess`) as a fallback. This ensures the UI remains responsive and verifiable even in restricted contexts like CI/CD pipelines.
