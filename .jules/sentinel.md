## 2026-03-24 - [Path Traversal in API Endpoints]
**Vulnerability:** API endpoints `/api/v1/run`, `/api/v1/search/setup`, and `/api/v1/gems/refine` were vulnerable to path traversal through `search_id`, `gem_id`, and `local_dir` parameters.
**Learning:** Using raw user input in file paths or directory creation, even when prefixed with a directory, can lead to traversal if the input contains `..` or leading `/`. FastAPI doesn't automatically sanitize path components in JSON payloads.
**Prevention:** Use Pydantic's `Field(pattern=...)` to restrict identifiers to a safe set of characters (excluding dots and path separators) and employ `os.path.basename()` as a secondary defensive layer for all ID-based file operations.
