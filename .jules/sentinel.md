## 2025-05-22 - Path Traversal in API Endpoints
**Vulnerability:** API endpoints that accepted identifiers (`search_id`, `candidate_id`, `gem_id`) used them directly in `os.path.join` or string formatting to access files. This allowed an attacker to use `../` to access files outside the intended directories (e.g., `prompts/`, `runs/`).
**Learning:** Pydantic models should always use strict regex validation for identifiers that are used in filesystem operations. Relying on default string types is insufficient when these strings influence file paths.
**Prevention:** Use a centralized `ID_PATTERN` (e.g., `r"^[a-zA-Z0-9_-]+$"`) and enforce it via Pydantic's `field_validator` in all request models that handle identifiers.
