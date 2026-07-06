## 2025-05-15 - Path Traversal in API Endpoints
**Vulnerability:** API endpoints (/api/v1/run, /api/v1/search/setup, /api/v1/gems/refine) allowed arbitrary strings for identifiers (search_id, gem_id, local_dir), enabling path traversal attacks.
**Learning:** Using raw user input to construct file system paths without validation is a critical security risk. Pydantic models lacked regex patterns and field validators.
**Prevention:** Enforce strict alphanumeric patterns for all ID-like fields using Pydantic's Field(pattern=...) and explicitly reject absolute paths or '..' components in directory strings.
