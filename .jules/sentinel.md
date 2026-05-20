## 2025-05-24 - Identifier Validation & Error Masking
**Vulnerability:** Path traversal via unvalidated identifiers (search_id, gem_id, entity_id) and information leakage through raw exception details in API responses.
**Learning:** Endpoints that construct file paths or database queries using user-provided IDs are susceptible to traversal if not strictly validated. Pydantic's `Field(pattern=...)` provides an efficient first line of defense. Raw exceptions can leak sensitive implementation details, including directory structures and database schemas.
**Prevention:** Use a centralized `ID_PATTERN` regex for all identifier fields in Pydantic models. Always catch and mask internal exceptions with generic user-friendly messages at the API boundary.
