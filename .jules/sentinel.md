## 2025-02-23 - API Input Validation for Directory Traversal Prevention
**Vulnerability:** Request endpoints (`/api/v1/run`, `/api/v1/search/setup`, `/api/v1/gems/refine`) accepted unvalidated string parameters (`search_id`, `candidate_id`, `gem_id`, `local_dir`) that were directly passed to `os.path.join` and file open calls, allowing directory traversal and arbitrary file overwrite.
**Learning:** Pydantic models without explicit validators default to accepting arbitrary string inputs, which can contain path traversal sequences (`..`, `/`, `\`).
**Prevention:** Use `@field_validator` on Pydantic request models to enforce strict regex patterns (`^[a-zA-Z0-9_-]+$`) on identifiers and path normalization checks on relative directory paths.
