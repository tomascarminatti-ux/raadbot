## 2025-05-23 - Centralized Identifier Validation
**Vulnerability:** Potential path traversal and injection attacks via unsanitized `search_id`, `entity_id`, and `trace_id` parameters used in file paths and database queries.
**Learning:** Identifiers were being used directly to construct file paths (e.g., `os.path.join("runs", search_id, ...)`) without validation, allowing attackers to potentially access or create files outside the intended directories using `../`.
**Prevention:** Implement a centralized `ID_PATTERN` (regex `^[a-zA-Z0-9_-]+$`) in `config.py` and enforce it using Pydantic `@field_validator` in all request models across the API and DB layers.
