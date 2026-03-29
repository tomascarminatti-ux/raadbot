## 2025-05-15 - Path Traversal in File Operations via API IDs
**Vulnerability:** User-provided IDs (`search_id`, `gem_id`, `candidate_id`) were used directly in `os.path.join` and f-strings to construct file paths, allowing directory traversal (e.g., `../../etc/passwd`).
**Learning:** Even with structured frameworks like FastAPI/Pydantic, string fields without explicit pattern validation are a major vector for path injection when used in file operations.
**Prevention:** Always use Pydantic's `Field(pattern=...)` to whitelist safe characters for identifiers and apply `os.path.basename()` as a defense-in-depth layer before file system calls.
