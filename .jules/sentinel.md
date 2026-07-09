## 2025-05-15 - Path Traversal in API Endpoints
**Vulnerability:** Path traversal via `search_id`, `gem_id`, and `local_dir` parameters in `/api/v1/run`, `/api/v1/search/setup`, and `/api/v1/gems/refine`.
**Learning:** FastAPI endpoints using `BaseModel` without explicit `pattern` or validators for string fields can allow malicious path components like `../`, leading to unauthorized file access or creation.
**Prevention:** Always use Pydantic's `Field(pattern=...)` for identifiers and implement `field_validator` for path-like strings to reject absolute paths and `..` components. Use `os.path.abspath` and prefix checking as defense-in-depth when constructing file paths from user input.
