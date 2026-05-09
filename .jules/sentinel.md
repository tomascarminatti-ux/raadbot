## 2025-05-15 - [improvement] Harden API input validation and prevent path traversal
**Vulnerability:** API endpoints were vulnerable to path traversal (via `local_dir` and `gem_id`) and lacked strict validation for identifier fields (`search_id`, `candidate_id`, `entity_id`, etc.).
**Learning:** Generic `str` types and `Dict[str, Any]` in Pydantic models for API endpoints can lead to security risks if the input is used in file system operations or database queries without proper sanitization/validation.
**Prevention:** Use Pydantic's `Field(pattern=...)` for regex-based validation of identifiers and `@field_validator` for complex validation like path safety. Always use strongly-typed Pydantic models for API endpoints.
