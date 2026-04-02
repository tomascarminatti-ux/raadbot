## 2025-04-02 - [SSRF & Path Traversal Prevention]
**Vulnerability:** API endpoints were susceptible to Path Traversal via IDs (search_id, gem_id) and SSRF via the `webhook_url` parameter.
**Learning:** For SSRF protection, simply checking the hostname string (e.g., "localhost") is insufficient as an attacker can use a custom domain pointing to a private IP. The server must resolve the hostname to an IP address and verify it against private/loopback ranges. For Path Traversal, FastAPI/Pydantic `Field(pattern=...)` provides a clean, declarative first line of defense at the schema level.
**Prevention:**
1. Use `pydantic.Field(pattern=r"^[a-zA-Z0-9_-]+$")` for all identifiers used in file paths.
2. Resolve all user-provided URLs using `socket.getaddrinfo()` and check the resulting IPs using `ipaddress.ip_address().is_private/is_loopback` before making outbound requests.
3. Apply `os.path.basename()` as a secondary defense layer before using user-controlled strings in `os.path.join()`.
