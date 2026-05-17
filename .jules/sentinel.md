## 2025-05-22 - Input Validation and Error Masking Pattern
**Vulnerability:** Identifier fields (search_id, entity_id, trace_id) and path fields (local_dir) were unvalidated, allowing potential directory traversal and information leakage through raw exception messages.
**Learning:** Using Pydantic v2 `Field(pattern=r"^[a-zA-Z0-9_-]+$")` provides a centralized and declarative way to harden identifiers. Catching general exceptions in FastAPI endpoints and returning generic messages (e.g., "Internal database error") prevents internal system details from leaking to users.
**Prevention:** Always apply standard regex patterns to identifier fields and use `@field_validator` for path-like strings to block `..` sequences. Mask detailed error responses in production-facing APIs.
