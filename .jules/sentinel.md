## 2025-05-15 - Path Traversal Prevention via Pydantic Validation

**Vulnerability:** Path traversal in API endpoints that construct file paths from user-provided identifiers (`search_id`, `gem_id`, `local_dir`, etc.).
**Learning:** Appending a file extension (e.g., `.md`) or a directory prefix is insufficient to prevent path traversal if the input is not validated against sequences like `../`. Strict regex validation at the schema level is a highly effective first line of defense.
**Prevention:** Enforce a strict alphanumeric pattern (`r'^[a-zA-Z0-9_-]+$'`) for all identifiers used in file-system operations using Pydantic's `Field(pattern=...)`. This avoids hardcoding whitelists while maintaining strong security boundaries.
