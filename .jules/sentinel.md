## 2025-06-06 - Path Traversal Protection and Whitelisting

**Vulnerability:** The `/api/v1/gems/refine` and `/api/v1/run` endpoints were vulnerable to path traversal because user-provided IDs (`gem_id`, `search_id`) were used directly in file path construction without adequate validation.

**Learning:** Implementing security fixes that involve file I/O can lead to accidental data loss during testing if reproduction scripts are not carefully isolated from production assets. A test intended to verify a fix for `refine_gem` accidentally overwrote a core prompt file because it was testing against the live filesystem instead of using mocks.

**Prevention:**
1. Use strict input validation (regex patterns) via Pydantic `Field(pattern=...)` to ensure identifiers only contain safe characters (alphanumeric, underscores, hyphens).
2. Implement a whitelist (`ALLOWED_GEMS`) for sensitive file access to ensure only authorized files can be modified.
3. Always mock filesystem operations (`os.path.exists`, `open`) and external service calls in security tests to prevent side effects on the development environment.
4. Ensure test scripts in the root directory use `if __name__ == "__main__":` guards to prevent accidental execution during `pytest` collection.
