# Sentinel's Journal - Critical Security Learnings

## 2025-05-20 - Strict Identifier and Webhook URL Validation in FastAPI Request Models
**Vulnerability:** Unsanitized user inputs (`search_id`, `candidate_id`, `gem_id`, `local_dir`, `webhook_url`) in API request models allowed potential directory traversal, arbitrary file writes/reads, and Server-Side Request Forgery (SSRF) targeting internal networks.
**Learning:** In Pydantic models, relying on basic `str` types without field validators allows inputs like `../` or `127.0.0.1` to reach underlying file operations and HTTP clients. Furthermore, `re.match` or `$` regexes can permit trailing newlines (`\n`), whereas `re.fullmatch(r"^[a-zA-Z0-9_-]+$")` guarantees exact alphanumeric filtering. `ipaddress.ip_address(host)` must explicitly catch `ValueError` when validating hostnames, specifically checking for IP property flags (`is_private`, `is_loopback`, `is_link_local`, `is_reserved`).
**Prevention:** Always attach `@field_validator` on Pydantic request models for any string parameter used in filesystem path construction or external network requests.
