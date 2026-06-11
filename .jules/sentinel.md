## 2025-05-22 - Path Traversal & Information Leakage in API
**Vulnerability:** Path traversal in `/api/v1/gems/refine` via `gem_id` and information leakage in `/api/v1/run` via raw exception messages.
**Learning:** Pydantic models without explicit pattern validation allowed arbitrary strings that could be used to construct malicious file paths. Catch-all exception handlers returning `str(e)` could expose internal configuration or database details.
**Prevention:** Always use `Field(pattern=...)` for identifiers used in file system operations. Implement a whitelist for sensitive operations like template/prompt refinement. Return generic error messages to external clients for unexpected exceptions.
