## 2025-05-22 - Path Traversal Protection and Error Hardening
**Vulnerability:** Path traversal in `gem_id`, `search_id`, and `candidate_id` could allow unauthorized file access. API error responses leaked internal exception details.
**Learning:** Using raw strings from API requests directly in `os.path.join` or file reading logic without strict pattern validation is a significant risk. Returning `str(e)` in FastAPI `HTTPException` can leak stack traces and internal paths.
**Prevention:** Use Pydantic's `Field(pattern=...)` for all identifier fields that interact with the filesystem. Implement explicit whitelists for sensitive file operations (like prompt refinement). Standardize error responses to generic messages for internal failures.
