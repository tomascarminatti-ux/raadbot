## 2025-06-04 - Path Traversal & Info Leakage via API
**Vulnerability:** Path traversal in `gem_id` and `search_id` parameters allowing arbitrary file reads/writes, and information leakage via verbose error messages.
**Learning:** Pydantic models without explicit pattern validation can accept characters like `../` which are dangerous when used to construct file paths. Additionally, exposing `str(e)` in API responses can leak internal paths and system architecture.
**Prevention:** Always use restrictive regex patterns (`ID_PATTERN`) in Pydantic `Field` for any identifier used in file paths. Implement explicit allow-lists for sensitive file access. Return generic error messages to clients while logging details internally.
