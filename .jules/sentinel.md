## 2026-08-19 - Path Traversal Protection via Pydantic Field Validation
**Vulnerability:** API endpoints accepting `search_id`, `candidate_id`, `gem_id`, and `local_dir` could be leveraged for path traversal attacks (`../`, absolute paths) when constructing output file paths or prompt template file reads.
**Learning:** Pydantic models with custom `@field_validator` hooks provide centralized defense-in-depth before application logic touches filesystem paths or passes identifiers to `os.path.join`.
**Prevention:** Use alphanumeric pattern matching (`^[a-zA-Z0-9_-]+$`) for IDs and normalize backslashes before checking for directory traversal (`..`) sequences in path strings.
