## 2025-01-24 - [Path Traversal in API Identifiers]
**Vulnerability:** Path traversal via `search_id` and `gem_id` in FastAPI endpoints allowed creating/modifying files outside of the intended `runs/` or `prompts/` directories.
**Learning:** Appending a file extension (e.g., `.md`) or a directory prefix is insufficient to prevent path traversal if the input is not validated against sequences like `../`.
**Prevention:** Use strict regex validation (e.g., `r'^[a-zA-Z0-9_-]+$'`) in Pydantic models for all identifiers that influence file paths, and implement whitelisting for sensitive identifiers.
