## 2025-05-14 - Hardening API against Path Traversal and Information Leakage
**Vulnerability:** API endpoints were using raw user-provided IDs (`search_id`, `gem_id`) to construct file paths without validation, and returning raw exception strings in error responses.
**Learning:** Pydantic models in FastAPI provide a powerful first line of defense via `Field(pattern=...)`. Combining this with `os.path.basename` provides robust protection against path traversal. Returning generic error messages (`HTTPException(detail="...")`) is essential to prevent leaking internal system details.
**Prevention:** Always use regex validation for identifiers that map to the file system or database. Always catch internal exceptions and return safe, generic messages to the client.
