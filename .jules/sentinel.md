## 2025-05-15 - Path Traversal in API Endpoints
**Vulnerability:** Path traversal allowed attackers to read or overwrite files outside intended directories by using `..` in request parameters like `gem_id`, `search_id`, and `local_dir`.
**Learning:** Pydantic models used for API requests did not have validation to restrict input that could be used in file path construction, creating a risk when those inputs were passed directly to `os.path.join`.
**Prevention:** Implement `field_validator` in Pydantic models to block directory traversal sequences (`..`), absolute paths, and drive letters for any parameter used in file system operations.
