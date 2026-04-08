## 2025-05-15 - [Path Traversal in API Identifiers]
**Vulnerability:** API endpoints accepted identifiers (`search_id`, `gem_id`) that were used directly in `os.path.join` and `open()` calls without validation, allowing arbitrary file read/write via `../` sequences.
**Learning:** Even if an ID is intended to be a simple string, without strict schema validation, it can be exploited as a path component.
**Prevention:** Enforce strict regex patterns (`r'^[a-zA-Z0-9_-]+$'`) for all identifier fields in Pydantic models and use `field_validator` to block `..` and absolute paths in any field representing a directory or file path.
