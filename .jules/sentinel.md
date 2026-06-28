## 2025-05-22 - Path Traversal Protection in Raadbot API
**Vulnerability:** Path Traversal via `search_id`, `local_dir`, `candidate_id`, and `gem_id`.
**Learning:** Appending a file extension (e.g., .md) or a directory prefix is insufficient to prevent path traversal if the input is not validated against sequences like '../'; strict regex validation (r'^[a-zA-Z0-9_-]+$') is required.
**Prevention:** Always validate identifiers used in file-path construction against a trusted pattern (e.g., `config.ID_PATTERN`) using Pydantic's `Field(pattern=...)`.
