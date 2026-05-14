## 2025-05-24 - API Hardening and Error Masking
**Vulnerability:** Information leakage via raw exception strings and potential path traversal/injection due to unvalidated identifiers.
**Learning:** FastAPI endpoints were catching generic `Exception` and returning `str(e)` in `HTTPException`, which leaks internal details (e.g., file paths, database structure). Additionally, Pydantic models lacked regex validation for identifier fields, and file-path-related fields lacked traversal checks.
**Prevention:** Always use Pydantic `Field(pattern=...)` for identifiers and implement custom `@field_validator` for path-like inputs. Use generic error messages in production-facing `HTTPException` responses while logging the detailed error internally.
