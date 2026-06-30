## 2025-05-15 - Strict Identifier Validation
**Vulnerability:** Path Traversal via `search_id`, `gem_id`, and `candidate_id` in API endpoints.
**Learning:** Using unsanitized string inputs directly in `os.path.join` or for file path construction allows attackers to access or modify files outside the intended directories (e.g., via `../`).
**Prevention:** Enforce strict allowlist validation for all identifiers using Pydantic's `pattern` argument and validate directory paths to reject absolute paths or components containing `..`.
