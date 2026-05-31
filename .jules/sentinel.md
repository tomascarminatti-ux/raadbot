## 2025-05-24 - Path Traversal and Information Leakage Mitigation
**Vulnerability:** Path traversal in `search_id` and `gem_id` allowed arbitrary directory creation and potential file access. API endpoints also leaked internal error details via `str(e)`.
**Learning:** Pydantic models without strict regex patterns or whitelists on string fields that are later used in file system operations are a common source of path traversal. Verbose error messages in `HTTPException` can expose sensitive internal state.
**Prevention:** Always use `Field(..., pattern=...)` or `@field_validator` for identifier strings. Centralize these patterns in a configuration file. Replace raw exception details with generic, safe error messages in production-facing APIs.
