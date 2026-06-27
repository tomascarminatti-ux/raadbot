## 2025-05-22 - Path Traversal via API Identifiers
**Vulnerability:** API endpoints using user-provided identifiers (`search_id`, `gem_id`, etc.) to construct file paths were vulnerable to path traversal (e.g., using `../`).
**Learning:** Appending extensions or directory prefixes is insufficient to prevent traversal if the input itself contains traversal sequences. Strict regex-based input validation at the schema level is a highly effective first line of defense.
**Prevention:** Use Pydantic's `Field(pattern=...)` with a strict whitelist pattern (like `r'^[a-zA-Z0-9_-]+$'`) for all identifier-like fields used in I/O operations.
