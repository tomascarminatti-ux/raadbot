## 2025-05-21 - Path Traversal & Info Leakage
**Vulnerability:** API endpoints allowed arbitrary string identifiers which could be used for path traversal (e.g., `../`) in file-related operations, and leaked internal exception details to the client.
**Learning:** Using f-strings or `os.path.join` with unsanitized user input for file paths is a high-risk pattern. Similarly, returning `str(e)` in an `HTTPException` can expose stack traces or environment details.
**Prevention:** Enforce strict regex validation for all identifiers using Pydantic's `Field(pattern=...)` and use an explicit whitelist for critical file access. Always return generic error messages for internal failures.
