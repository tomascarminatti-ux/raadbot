## 2026-03-07 - Path Traversal Prevention in API Endpoints
**Vulnerability:** API endpoints accepted unsanitized identifiers (`search_id`, `candidate_id`, `gem_id`) and directory paths (`local_dir`), allowing potential path traversal attacks (e.g., `../../etc/passwd`).
**Learning:** FastAPI's default Pydantic models allow any string if not explicitly constrained, which can lead to file system vulnerabilities when these strings are used in `os.path.join` or `open()`.
**Prevention:** Use Pydantic's `Field(pattern=...)` with strict regex (e.g., `^[a-zA-Z0-9_-]+$`) for identifiers and `field_validator` to block dangerous sequences like `..` in path-like fields.
