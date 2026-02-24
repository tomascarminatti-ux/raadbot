## 2025-05-15 - [Path Traversal and SSRF Protection in API]
**Vulnerability:** Endpoints in `api.py` were vulnerable to path traversal (via `search_id`, `candidate_id`, `local_dir`, `gem_id`) and SSRF (via `webhook_url`).
**Learning:** Pydantic models lacked validation for these sensitive fields, which are directly used in file system operations and outgoing HTTP requests.
**Prevention:** Use Pydantic `field_validator` with `mode="before"` to sanitize inputs. Block `..`, absolute paths, and private IP ranges for webhooks.
