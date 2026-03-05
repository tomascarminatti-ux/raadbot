## 2025-05-14 - Path Traversal Prevention in API Request Models
**Vulnerability:** Path traversal in `PipelineRequest`, `SetupSearchRequest`, and `RefineRequest` via `search_id`, `gem_id`, and `local_dir`.
**Learning:** FastAPI endpoints that use user-provided strings to construct file paths are vulnerable if those strings are not validated against traversal sequences (like `..`) or restricted to a safe character set.
**Prevention:** Use Pydantic's `Field(pattern=...)` to enforce strict alphanumeric identifiers and `@field_validator` to block path traversal markers and absolute paths in directory fields.
