## 2025-05-15 - [Path Traversal and SSRF Protection in API]
**Vulnerability:** Endpoints in `api.py` were vulnerable to path traversal (via `search_id`, `candidate_id`, `local_dir`, `gem_id`) and SSRF (via `webhook_url`).
**Learning:** Pydantic models lacked validation for these sensitive fields, which are directly used in file system operations and outgoing HTTP requests.
**Prevention:** Use Pydantic `field_validator` with `re.fullmatch` on identifiers to prevent path traversal, normalize path separators and reject relative path sequences (`..`) or absolute paths on directories, and validate schemes and block internal/loopback/private IP addresses for webhooks.
