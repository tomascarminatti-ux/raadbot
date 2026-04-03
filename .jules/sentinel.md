## 2025-05-22 - SSRF Protection with Pydantic and IPAddress
**Vulnerability:** Server-Side Request Forgery (SSRF) via `webhook_url` parameter.
**Learning:** Pydantic's `HttpUrl` validates format but not destination. `ipaddress` module is needed to reliably check if a host is private or loopback, especially when it might be an IP literal.
**Prevention:** Always use a validator with `ipaddress.ip_address` check and fallback to hostname blacklisting (localhost, etc.) for `HttpUrl` fields that trigger outbound requests.

## 2025-05-22 - Defense in Depth for Path Traversal
**Vulnerability:** Path traversal via user-controlled IDs (search_id, gem_id, candidate_id) used in file paths.
**Learning:** Regex validation (`^[a-zA-Z0-9_-]+$`) in Pydantic models is the first line of defense. `os.path.basename()` provides a secondary layer in case validation is bypassed or misconfigured in future updates.
**Prevention:** Combine input validation (strict regex) with path sanitization (`os.path.basename`) before using user input in `os.path.join` or file operations.
