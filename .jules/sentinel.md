## 2025-05-15 - [Path Traversal in GEM Identifiers]
**Vulnerability:** User-provided `gem_id` and `search_id` were used to construct file paths without validation, allowing potential path traversal (e.g., `../../etc/passwd`).
**Learning:** Appending a file extension (e.g., `.md`) or a prefix directory is insufficient protection if the identifier contains `../` sequences.
**Prevention:** Enforce strict regex validation (e.g., `r"^[a-zA-Z0-9_-]+$"` via Pydantic `Field(pattern=...)`) and use explicit whitelists for sensitive identifiers like GEM IDs.
