## 2026-02-25 - Input Validation and Security Headers in Raadbot API
**Vulnerability:** Path Traversal in `search_id`, `local_dir`, `candidate_id`, and `gem_id`; SSRF in `webhook_url`; Missing security headers.
**Learning:** Pydantic `field_validator` provides a clean way to centralize input validation for API models, preventing common vulnerabilities like path traversal and SSRF before they reach the business logic.
**Prevention:** Use `field_validator` for any field that interacts with the file system or makes external network requests. Always include security headers middleware in FastAPI apps.
