## 2025-05-14 - Path Traversal Prevention in API Endpoints
**Vulnerability:** Path traversal via user-provided identifiers (`search_id`, `gem_id`) used to construct filesystem paths or open files.
**Learning:** Appending a file extension (e.g., '.md') to a user-provided identifier is insufficient protection; mandatory regex validation against a safe pattern (r'^[a-zA-Z0-9_-]+$') and explicit whitelisting for critical files are required.
**Prevention:** Use Pydantic's `Field(..., pattern=config.ID_PATTERN)` for all identifier inputs and maintain a dynamic whitelist for sensitive file lookups (like GEM prompts).
