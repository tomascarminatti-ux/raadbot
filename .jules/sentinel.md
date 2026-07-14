## 2025-05-22 - Path Traversal in API Identifiers
**Vulnerability:** API endpoints using user-provided IDs (`search_id`, `gem_id`) were vulnerable to path traversal because these IDs were directly concatenated into file paths without validation.
**Learning:** Even internal-facing APIs can expose file systems if identifiers aren't strictly validated against a safe character whitelist.
**Prevention:** Use Pydantic's `field_validator` with a strict regex (e.g., `^[a-zA-Z0-9_-]+$`) to ensure identifiers contain only safe characters before they are used in path construction.
