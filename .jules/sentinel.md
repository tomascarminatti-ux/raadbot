## 2025-05-24 - Input Validation for Path Identifiers
**Vulnerability:** Potential path traversal via unsanitized search_id and gem_id in API requests.
**Learning:** Identifiers used to construct file paths (e.g., in runs/ or prompts/) were accepted as raw strings without validation, allowing directory traversal sequences like "../".
**Prevention:** Enforce strict regex validation (e.g., ^[a-zA-Z0-9_-]+$) on all identifier fields in Pydantic models and use whitelists for restricted sets of values like GEM IDs.
