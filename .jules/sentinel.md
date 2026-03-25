## 2025-03-25 - Path Traversal in API Endpoints
**Vulnerability:** User-controlled IDs (`search_id`, `gem_id`, `candidate_id`) were used to construct file paths without validation or sanitization, allowing arbitrary file read/write via `../` sequences.
**Learning:** Even internal APIs can be vulnerable to path traversal if they interact with the filesystem. Pydantic models provide a first line of defense through regex validation, but `os.path.basename()` should always be used as defense-in-depth when constructing paths from user input.
**Prevention:** Always use `Field(pattern=...)` in Pydantic models to restrict allowed characters in ID-like fields. Sanitize path components using `os.path.basename()` before joining them with base directories.
