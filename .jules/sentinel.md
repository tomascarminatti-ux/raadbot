## 2026-03-31 - Path Traversal Prevention in API Request Models
**Vulnerability:** API endpoints accepting `search_id`, `candidate_id`, `gem_id`, and `local_dir` were vulnerable to path traversal attacks (`../`) and arbitrary directory manipulation when handling file system paths and reading/writing prompt files or output directories.
**Learning:** Pydantic request models without strict string patterns or path sanitization can allow untrusted input strings containing directory traversal components to propagate directly into `os.path.join` and `open()` calls.
**Prevention:** Implement strict alphanumeric validation (`^[a-zA-Z0-9_-]+$`) for identifier inputs and path normalization checks on directory path arguments across all API request models using `@field_validator`.
