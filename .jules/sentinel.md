## 2025-05-14 - Path Traversal via Absolute Paths in os.path.join
**Vulnerability:** Path traversal via `search_id` or `local_dir` fields in API requests.
**Learning:** In Python's `os.path.join`, if a component is an absolute path (e.g., starts with `/`), it overrides all previous components. Validating for `..` is not enough; strict validation of the entire string is required to prevent bypassing base directories.
**Prevention:** Enforce a strict regex pattern (e.g., `^[a-zA-Z0-9_-]+$`) for all user-supplied identifiers that are used in path construction.
