## 2025-05-15 - [Path Traversal in API Requests]
**Vulnerability:** User-provided inputs (search_id, gem_id, local_dir) were used to construct file paths without validation, allowing for path traversal (e.g., using '..' or absolute paths).
**Learning:** Pydantic models in FastAPI provide a powerful first line of defense. Using `Field(pattern=...)` for identifiers and `field_validator` for paths can effectively block traversal attempts before they reach the logic layer.
**Prevention:** Always validate string inputs used in file system operations. Restrict identifiers to safe character sets (alphanumeric, underscores, hyphens) and reject any path components containing '..' or absolute paths.
