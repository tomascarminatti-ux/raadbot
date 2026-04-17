## 2026-04-17 - Path Traversal in API Identifiers
**Vulnerability:** Path traversal vulnerability in `api.py` where `search_id`, `gem_id`, and `candidate_id` were used to construct file paths (via `os.path.join`) without validation.
**Learning:** In Python, `os.path.join()` returns an absolute path if any component is an absolute path. Furthermore, without character restriction, an attacker can use `..` to access files outside the intended directory.
**Prevention:** Implement strict regex validation for all identifier fields in Pydantic models. Restricting these to `^[a-zA-Z0-9_-]+$` ensures they remain safe for use in filesystem and database operations.
