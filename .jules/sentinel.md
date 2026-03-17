## 2025-05-14 - Path Traversal in GEM Refinement and Pipeline Run
**Vulnerability:** The `/api/v1/gems/refine` and `/api/v1/run` endpoints allowed arbitrary file read/write access via `gem_id` and `search_id` parameters due to lack of input validation before path concatenation.
**Learning:** Using user-provided strings directly in `os.path.join` or f-string paths without strict alphanumeric validation is a high-risk pattern in this codebase.
**Prevention:** Always enforce strict regex validation (e.g., `^[a-zA-Z0-9_-]+$`) on identifiers used in file system operations via Pydantic models.
