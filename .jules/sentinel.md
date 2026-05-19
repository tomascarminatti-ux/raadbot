## 2025-05-24 - Identifier Validation & Error Masking
**Vulnerability:** Information leakage through raw exception messages and potential path traversal via unsanitized identifiers used in file system operations.
**Learning:** FastAPI endpoints were returning `str(e)` on failure, exposing internal structure. Identifiers like `search_id` were used in `os.path.join` without validation, allowing directory traversal.
**Prevention:** Centralize regex validation for identifiers in `config.py`. Use Pydantic `Field(pattern=...)` for automatic input sanitization. Mask exceptions with generic messages for external clients while maintaining internal integrity.
