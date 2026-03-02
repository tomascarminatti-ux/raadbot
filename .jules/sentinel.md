## 2025-05-15 - Path Traversal and Input Validation in FastAPI Endpoints
**Vulnerability:** Path traversal in `search_id`, `local_dir`, and `gem_id` parameters across several API endpoints.
**Learning:** FastAPI's `BaseModel` without explicit `Field` constraints or `field_validator` logic allows arbitrary strings, which were being used directly in `os.path.join` and file path construction.
**Prevention:** Always use Pydantic `Field(pattern=...)` for identifiers and implement `field_validator` to block dangerous sequences like `..` or absolute paths when handling file-system related inputs.
