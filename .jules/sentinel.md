## 2025-05-14 - API Security Hardening

**Vulnerability:** Path Traversal and SSRF in API endpoints.
**Learning:** The application allowed arbitrary file system access through `search_id` and `local_dir` parameters because they were directly concatenated into file paths without validation. It also allowed SSRF via the `webhook_url` parameter.
**Prevention:** Use Pydantic's `Field(pattern=...)` and `@field_validator` to enforce strict input validation for all API parameters used in file operations or network requests. Always block `..` sequences and absolute paths for file operations, and block local/private IP ranges for webhooks.
