## 2025-05-15 - Path Traversal Prevention in API Endpoints
**Vulnerability:** Path traversal via `search_id`, `gem_id`, and `local_dir` parameters in FastAPI endpoints.
**Learning:** Using `os.path.join` with user-controlled input without validation can allow access to sensitive files or creation of directories outside intended paths. In Pydantic v2, `Field(pattern=...)` and `@field_validator` provide a robust way to enforce identifier formats and block dangerous sequences.
**Prevention:** Restrict identifiers to alphanumeric characters, underscores, and hyphens. Use a custom validator to block '..', absolute paths, and drive indicators in path-like parameters.
