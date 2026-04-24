## 2025-05-15 - Input Validation Hardening with Pydantic
**Vulnerability:** Path traversal and identifier injection in API and DB endpoints.
**Learning:** Identifier fields like `search_id` and `gem_id` were used in file path construction (e.g., `os.path.join("runs", search_id)`) without validation, allowing potential access to files outside the intended directories.
**Prevention:** Use Pydantic's `Field(pattern=...)` to restrict identifiers to alphanumeric characters and implement `@field_validator` for path fields to block traversal sequences like `..` at the schema level.
