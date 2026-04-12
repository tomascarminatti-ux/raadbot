## 2025-05-22 - [Path Traversal in API]
**Vulnerability:** The API endpoints (`/api/v1/run`, `/api/v1/search/setup`, `/api/v1/gems/refine`) were vulnerable to path traversal because they accepted `search_id`, `gem_id`, and `local_dir` without validation. These values were used to construct file paths for directory creation and file reading/writing.
**Learning:** Pydantic models in FastAPI provide a powerful and idiomatic way to enforce security constraints on incoming data early in the request lifecycle.
**Prevention:** Always use `Field(pattern=...)` for identifiers and custom `field_validator` for path-like strings to ensure they are relative and contain no traversal sequences.
