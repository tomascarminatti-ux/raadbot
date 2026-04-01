## 2025-05-15 - SSRF Protection with Hostname Fallback
**Vulnerability:** Server-Side Request Forgery (SSRF) via webhook_url parameter.
**Learning:** When implementing SSRF protection using `ipaddress.ip_address()`, a common pattern is to catch `ValueError` to allow hostnames. However, if the `is_private` check itself raises an exception or if the logic is not careful, a private IP could be mistakenly treated as a hostname and bypass the check.
**Prevention:** Explicitly re-raise `ValueError` when it originates from the security check itself (e.g., "Private or reserved IP addresses are not allowed") to ensure it doesn't fall through to the hostname "pass" block.
