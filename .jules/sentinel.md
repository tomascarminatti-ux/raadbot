## 2025-05-15 - [CRITICAL] Fix path traversal in API endpoints
**Vulnerability:** Path traversal via unsanitized `gem_id`, `search_id`, and `local_dir` parameters.
**Learning:** Frameworks like FastAPI don't automatically sanitize strings used for file paths. Pydantic `field_validator` provides a centralized way to enforce strict ID patterns and block traversal sequences.
**Prevention:** Use a strict whitelist regex (e.g., `r"^[a-zA-Z0-9_-]+$"`) for all ID-like fields used in filesystem operations and explicitly validate that directory paths are relative and do not contain `..`.
