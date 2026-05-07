## 2025-05-15 - Path Traversal via Unvalidated Pydantic Fields
**Vulnerability:** The `/api/v1/gems/refine` endpoint allowed arbitrary file writes by passing `../` in the `gem_id` field, which was directly used to construct a file path for `open(..., "w")`.
**Learning:** Even when using Pydantic models, fields must be explicitly validated with regex or custom validators if they are used to construct file system paths or database queries. Default string types are overly permissive.
**Prevention:** Use `Field(pattern=r"^[a-zA-Z0-9_-]+$")` for all identifier fields used in path construction and implement `@field_validator` for path components to block traversal sequences (`..`, `/`, `:`).
