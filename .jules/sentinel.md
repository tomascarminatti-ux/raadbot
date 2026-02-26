## 2025-05-22 - Path Traversal and SSRF Mitigation in FastAPI Models

**Vulnerability:** Input fields like `search_id`, `local_dir`, and `webhook_url` were used directly in file system operations or network requests without validation.
**Learning:** Pydantic models in FastAPI provide a clean way to implement centralized validation using `field_validator`. When implementing SSRF protection, the hostname must be carefully extracted and validated against both hostnames (localhost) and IP ranges (private/loopback).
**Prevention:** Always use `field_validator` to block '..' and absolute paths for any input used in `os.path.join`. For webhooks, use `ipaddress` to verify the resolved destination is not in a private or loopback range.
