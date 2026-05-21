## 2025-05-22 - Path Traversal & Info Leakage Hardening
**Vulnerability:** API endpoints were susceptible to path traversal via `search_id` and `gem_id` fields, and leaked internal stack traces in `HTTPException` responses.
**Learning:** Generic `str` types in Pydantic models without pattern validation allow malicious path components like `../`. Masking errors without logging makes debugging impossible.
**Prevention:** Use strict regex patterns (e.g., `^[a-zA-Z0-9_-]+$`) for all identifier fields in Pydantic models. Always log raw exceptions on the server before returning generic error messages to the client.
