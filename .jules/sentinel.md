## 2025-05-22 - [Path Traversal in GEM Refinement]
**Vulnerability:** The `/api/v1/gems/refine` endpoint used the user-provided `gem_id` to construct a file path without sufficient validation, allowing for potential path traversal (e.g., `../filename`).
**Learning:** Appending a file extension (like `.md`) is not a sufficient defense against path traversal if the directory structure is not strictly enforced.
**Prevention:** Always validate identifiers against a safe regex (like `^[a-zA-Z0-9_-]+$`) and use an explicit whitelist for files that are allowed to be accessed or modified by the application logic.
