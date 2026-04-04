## 2025-05-15 - [Path Traversal Prevention via Pydantic Validation]
**Vulnerability:** User-provided `search_id`, `gem_id`, and `local_dir` were used to construct file system paths without sufficient validation, allowing for path traversal attacks (e.g., using `..` to access or create files outside intended directories).
**Learning:** FastAPI/Pydantic models provide a declarative way to enforce security constraints on inputs via regex patterns. Restricting allowed characters is a more robust defense than manual sanitization or "blacklisting" specific sequences.
**Prevention:** Always validate identifiers that will be used in file paths using strict regex patterns (e.g., `^[a-zA-Z0-9_-]+$`). For paths that must allow subdirectories, restrict the use of dots to prevent traversal.
