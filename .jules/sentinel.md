## 2025-02-22 - Path Traversal in API Endpoints
**Vulnerability:** API endpoints using user-provided IDs (`search_id`, `candidate_id`, `gem_id`) to construct file paths were vulnerable to path traversal. An attacker could use `..` sequences to write or read files outside the intended directories (e.g., `runs/` or `prompts/`).
**Learning:** Using `os.path.join` with unsanitized user input is dangerous as it allows escaping the base directory.
**Prevention:** Use Pydantic `field_validator` to sanitize and validate all string inputs used in path construction, blocking `..`, `/`, and `\` sequences.

## 2025-02-22 - SSRF in Webhook Callback
**Vulnerability:** The `webhook_url` parameter in the `/api/v1/run` endpoint allowed any URL, enabling Server-Side Request Forgery (SSRF). An attacker could point the callback to internal services or the application itself.
**Learning:** Accepting arbitrary URLs for callbacks without validation exposes the internal network.
**Prevention:** Implement a validator for URL parameters that blocks localhost and private IP ranges.
