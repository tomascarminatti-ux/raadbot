## 2025-05-15 - [Path Traversal via Unvalidated Identifiers]
**Vulnerability:** Path traversal via `search_id` and `gem_id` in API endpoints (`/api/v1/search/setup`, `/api/v1/gems/refine`). An attacker could use `../` to access or overwrite files outside the intended directories.
**Learning:** Appending a file extension (e.g., '.md') to a user-provided identifier is insufficient protection against path traversal.
**Prevention:** Enforce a strict regex pattern (e.g., `r'^[a-zA-Z0-9_-]+$'`) on all identifiers used in file system operations and use explicit whitelisting for sensitive identifiers like GEM IDs.
