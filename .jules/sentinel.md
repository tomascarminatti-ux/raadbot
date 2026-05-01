## 2025-05-14 - Path Traversal Protection via Pydantic Validation
**Vulnerability:** API endpoints were accepting arbitrary strings for identifiers like `search_id` and `gem_id`, which were subsequently used in file path construction (e.g., `os.path.join` or f-strings), enabling path traversal attacks.
**Learning:** Pydantic models without explicit validation patterns are overly permissive, allowing ".." and absolute paths to bypass intended directory restrictions before reaching application-level logic.
**Prevention:** Use Pydantic's `Field(pattern=...)` for regex-based identifier validation and `@field_validator` for complex path-related inputs to explicitly reject `..` and absolute paths at the request validation layer.
