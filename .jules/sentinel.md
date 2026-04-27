## 2025-05-15 - Input Validation Hardening
**Vulnerability:** Lack of input validation on identifier fields (`search_id`, `gem_id`, `entity_id`) that were used directly in `os.path.join` and database queries, creating a path traversal and injection risk.
**Learning:** Even if an application is intended for internal use, trusting identifiers from requests is dangerous. Pydantic's `pattern` and `field_validator` provide a clean, declarative way to enforce "allow-listing" at the edge of the system.
**Prevention:** Always restrict identifiers used for filesystem or database operations to a strict alphanumeric/safe-character regex and explicitly block traversal sequences like `..`.
