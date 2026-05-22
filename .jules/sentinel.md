## 2025-05-24 - [HIGH] Path Traversal and Information Leakage in API
**Vulnerability:** The `refine_gem` endpoint was vulnerable to path traversal via the `gem_id` parameter. Multiple endpoints leaked internal exception details to the client through `str(e)`.
**Learning:** Using unsanitized user input to construct file paths is a classic vulnerability that persists when developers prioritize flexibility over security. Returning raw exceptions in production APIs is a common source of information leakage.
**Prevention:** Centralize security constants like `ALLOWED_GEMS` and `ID_PATTERN`. Use Pydantic `@field_validator` for all identifier inputs. Always log raw errors internally and return generic messages to the end-user.
