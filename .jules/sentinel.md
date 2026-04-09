## 2025-05-15 - API Path Traversal & Identifier Injection
**Vulnerability:** API endpoints (`/api/v1/run`, `/api/v1/search/setup`, `/api/v1/gems/refine`) accepted unvalidated strings for identifiers (`search_id`, `gem_id`) and directory paths (`local_dir`). This allowed for path traversal (e.g., `../../etc`) and arbitrary directory creation or file access.
**Learning:** Even internal-facing APIs can be exploited if they interact with the filesystem using user-provided strings. Pydantic models should be the first line of defense using `Field(pattern=...)` and `field_validator`.
**Prevention:** Always validate identifiers against strict alphanumeric/hyphen patterns and use `os.path.isabs()` + checking for `..` in any user-provided path fragments.
