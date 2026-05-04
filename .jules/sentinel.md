## 2025-05-15 - Path Traversal in Prompt Refinement
**Vulnerability:** The `/api/v1/gems/refine` endpoint was vulnerable to path traversal because it used the `gem_id` directly in a file path without validation, allowing arbitrary file reading/writing via `../` patterns.
**Learning:** Even with Pydantic models, identifier fields should have strict regex patterns (`r"^[a-zA-Z0-9_-]+$"`) to prevent directory traversal characters. For endpoints that touch the file system, a whitelist of allowed files provides a secondary layer of defense (Defense in Depth).
**Prevention:** Always use regex validation for ID fields in Pydantic models and implement whitelisting or path resolution checks (e.g., `pathlib.Path.resolve()`) for any input used to construct file paths.
