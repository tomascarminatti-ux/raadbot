## 2025-05-15 - Path Traversal in API Identifiers
**Vulnerability:** API endpoints (`/api/v1/run`, `/api/v1/search/setup`, `/api/v1/gems/refine`) accepted identifiers (`search_id`, `candidate_id`, `gem_id`) that were used directly in file system paths without validation, allowing for potential path traversal attacks (e.g., using `../` to access or create files outside intended directories).
**Learning:** Even internal or non-public APIs must strictly validate identifiers used in constructing file paths (using whitelists/regex) to prevent unauthorized file system exposure and manipulation.
**Prevention:** Use Pydantic's `field_validator` with a restrictive regex pattern (e.g., `^[a-zA-Z0-9_-]+$`) to centralize input sanitization for all ID fields used in file paths.
