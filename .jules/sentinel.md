## 2025-05-15 - [Path Traversal in API Models]
**Vulnerability:** Input fields like `search_id` and `local_dir` in `api.py` were used to construct file paths without validation, allowing directory traversal (e.g., `../`).
**Learning:** Even with Pydantic models, default `str` types are too permissive for identifiers that interact with the filesystem.
**Prevention:** Use Pydantic's `Field(pattern=...)` for strict regex validation of identifiers and `field_validator` for path-specific checks like `os.path.isabs()` and `..` sequence detection.
