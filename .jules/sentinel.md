## 2026-06-16 - Path Traversal Prevention via Pydantic and Whitelisting
**Vulnerability:** Path traversal in the `/api/v1/gems/refine` endpoint allowed reading/writing arbitrary files by manipulating the `gem_id` parameter.
**Learning:** Appending a file extension (e.g., '.md') to a user-provided identifier is insufficient protection against path traversal as `../` sequences can still navigate the filesystem.
**Prevention:** Implement mandatory regex validation (e.g., `r"^[a-zA-Z0-9_-]+$"` via Pydantic `Field(pattern=...)`) for all identifiers used in file paths and enforce an explicit whitelist for critical filesystem operations.
