## 2025-05-22 - API Input Hardening and Error Masking
**Vulnerability:** Path traversal and injection via unvalidated identifier fields (e.g., `search_id`, `gem_id`) and information leakage through raw exception details in HTTP responses.
**Learning:** Using Pydantic's `Field(pattern=...)` provides a clean, declarative way to enforce strict input validation at the API entry point. Masking errors by replacing `str(e)` with generic messages in `HTTPException` prevents leaking internal application logic.
**Prevention:** Always use regex validation for identifiers and avoid returning raw exception strings in production APIs. Use Pydantic models instead of generic `Dict` for incoming request payloads to ensure type safety and automatic validation.
