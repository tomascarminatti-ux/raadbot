## 2025-05-22 - Path Traversal and Identifier Injection in API
**Vulnerability:** Lack of input validation in `api.py` endpoints (`/api/v1/run`, `/api/v1/search/setup`, `/api/v1/gems/refine`) allowed for potential path traversal via `local_dir` and malformed identifiers in `search_id`, `candidate_id`, and `gem_id`.
**Learning:** Pydantic models without `Field` constraints or validators only check types, not the content of strings, which can lead to security risks when those strings are used in file system operations or command construction.
**Prevention:** Use Pydantic `Field(pattern=...)` for all identifier-like fields to restrict allowed characters, and implement custom `@field_validator` to block dangerous path sequences like `..`.
