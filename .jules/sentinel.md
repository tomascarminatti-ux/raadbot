## 2025-04-26 - Identifier and Path Hardening
**Vulnerability:** Identifier fields (e.g., `search_id`, `gem_id`) and path fields (e.g., `local_dir`) in Pydantic models were unvalidated, accepting path traversal sequences like `../../`.
**Learning:** Default Pydantic string fields are overly permissive. Without explicit `Field(pattern=...)` or `field_validator`, an application is vulnerable to path traversal if these strings are used in file system operations (like `os.path.join`).
**Prevention:** Always apply restrictive regex patterns (`^[a-zA-Z0-9_-]+$`) to identifier fields and use custom validators to explicitly reject traversal patterns (`..`) and absolute paths in any field representing a relative directory or filename.
