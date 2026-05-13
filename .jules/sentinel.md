## 2025-05-15 - Input Validation and Error Masking
**Vulnerability:** Multiple endpoints in `api.py` and `infra/db/api.py` lacked strict input validation for identifiers and file paths, and unhandled exceptions were leaking internal details to clients.
**Learning:** Even internal-facing APIs (like the DB API) should implement strict input validation and error masking. Pydantic models with regex patterns are an effective first line of defense.
**Prevention:** Use `Field(pattern=r"^[a-zA-Z0-9_-]+$")` for all identifier fields and always catch exceptions to return generic 400/500 error messages instead of raw exception strings.
