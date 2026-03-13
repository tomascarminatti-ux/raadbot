# Sentinel Security Journal

## 2025-05-14 - Path Traversal via Unsanitized Identifiers
**Vulnerability:** Path traversal in `api.py` (`setup_search`, `run_pipeline`) and `infra/db/api.py` due to lack of validation on `search_id`, `entity_id`, and `local_dir`.
**Learning:** Using `os.path.join` with user-controlled strings that may contain `..` or start with `/` allows writing/reading files outside the intended directory.
**Prevention:** Use Pydantic's `Field(pattern=...)` or custom validators to restrict identifiers to safe characters (alphanumeric, hyphens, underscores) and explicitly check for traversal sequences in path-like inputs.
