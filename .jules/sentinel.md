# Sentinel Security Journal 🛡️

## 2025-06-24 - ID Validation for Path Traversal Prevention
**Vulnerability:** API endpoints accepted arbitrary strings for identifiers like `search_id` and `gem_id`, which were used directly in file path construction.
**Learning:** Appending a file extension or directory prefix is insufficient to prevent path traversal if the input contains sequences like `../`.
**Prevention:** Enforce a strict regex pattern (e.g., `^[a-zA-Z0-9_-]+$`) in Pydantic models for all identifiers used in file-system operations. Additionally, use whitelisting for sensitive file access.
