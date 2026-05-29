## 2025-05-24 - Path Traversal & Information Leakage Mitigation
**Vulnerability:** API endpoints (`/api/v1/gems/refine`, `/api/v1/run`, `/api/v1/search/setup`) were vulnerable to path traversal via unsanitized `gem_id` and `search_id` fields. Additionally, internal exception details were leaked to clients via `str(e)` in `HTTPException`.
**Learning:** Using user-provided strings directly in file paths is a critical risk. Pydantic's `Field(pattern=...)` and `@field_validator` provide a robust first line of defense for input sanitization.
**Prevention:** Implement a centralized `ID_PATTERN` and whitelists for all user-provided identifiers. Always use generic error messages for external-facing APIs.
