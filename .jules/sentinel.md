## 2025-05-14 - Path Traversal via Untrusted Identifiers
**Vulnerability:** Path traversal in `/api/v1/gems/refine` and potential traversal in endpoints using `search_id`.
**Learning:** Appending a file extension (e.g., '.md') to a user-provided identifier is insufficient protection against path traversal if the identifier contains `../`. Pydantic models should enforce strict regex patterns for all identifiers that are used to construct file system paths.
**Prevention:** Always use a strict regex like `r"^[a-zA-Z0-9_-]+$"` for identifiers and implement whitelisting for sensitive file access.
