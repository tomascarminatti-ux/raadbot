# Sentinel Journal - Security Learnings

## 2025-05-14 - Improved SSRF and Path Traversal Protection
**Vulnerability:** Path Traversal and SSRF in API endpoints.
**Learning:** Naive regex matching for SSRF (e.g., matching "10." anywhere) causes false positives in URL paths (e.g., `v10.1`). Using `urllib.parse.urlparse` to isolate the hostname is more precise. Also, path traversal checks must include Windows drive letters (e.g., `C:`) in addition to `..` and leading slashes.
**Prevention:** Always use `urlparse` for URL validation and include `re.match(r'^[a-zA-Z]:', v)` for path validation in cross-platform applications.
