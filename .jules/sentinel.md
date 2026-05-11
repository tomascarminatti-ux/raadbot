## 2025-05-15 - Input Hardening and Path Traversal Prevention
**Vulnerability:** The API endpoints were susceptible to path traversal via the `local_dir` parameter and potential injection or unauthorized file access via unvalidated identifier fields (`search_id`, `entity_id`, etc.). Additionally, raw exception strings were being returned to the user, leaking implementation details.

**Learning:** Relying on basic string inputs for file-system-related parameters without strict validation or sandboxing allows attackers to escape the intended directory scope. Furthermore, using unvalidated identifiers in file paths (`os.path.join("runs", search_id, ...)`) can lead to unintended file operations if the identifier contains traversal sequences like `../`.

**Prevention:**
1. Use Pydantic's `Field(pattern=...)` to enforce strict alphanumeric (plus underscore/dash) validation for all identifier fields.
2. Implement custom validators (`@field_validator`) for path-like parameters to explicitly block traversal sequences (`..`) and absolute paths.
3. Mask internal application errors by returning generic error messages to the client while keeping detailed logs server-side.
4. Replace raw dictionary inputs with strictly typed Pydantic models for all internal API communication to ensure schema enforcement at the boundary.
