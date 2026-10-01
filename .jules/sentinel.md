## 2026-02-25 - Pydantic Field Validation for Path Traversal & SSRF Prevention
**Vulnerability:** API endpoints accepted unvalidated strings (`search_id`, `gem_id`, `candidate_id`, `local_dir`, `webhook_url`) allowing path traversal file access/writes and SSRF requests to loopback/private IP addresses or cloud metadata services.
**Learning:** Using `re.fullmatch(r"[a-zA-Z0-9_-]+", v)` prevents newline or special character injection in identifiers. Isolating `ipaddress.ip_address()` calls ensures custom `raise ValueError(...)` assertions are not inadvertently caught in broad exception handlers.
**Prevention:** Always enforce strict alphanumeric regex checks on path identifiers and filter webhooks against loopback, private, link-local, and reserved IP ranges via Pydantic `field_validator`s.
