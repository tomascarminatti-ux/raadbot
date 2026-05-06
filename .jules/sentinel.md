## 2025-05-15 - Input Validation & Path Traversal Protection
**Vulnerability:** Lack of input validation on API identifier fields (`search_id`, `gem_id`) and directory path fields (`local_dir`) allowed for potential path traversal and unintended file system access.
**Learning:** FastAPI request models without explicit regex constraints or custom validators trust user input by default, which is dangerous when that input is used to construct file paths or database identifiers. Pydantic v2 requires `Field(pattern=...)` for regex and `@field_validator` for logic-based checks.
**Prevention:** Always apply the `r"^[a-zA-Z0-9_-]+$"` pattern to identifier fields and use a dedicated `field_validator` to block `..`, absolute paths, and drive letters in fields that represent local file system paths.
