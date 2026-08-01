## 2026-08-01 - Path Traversal Vulnerabilities in Raadbot Gateway Endpoints
**Vulnerability:** Arbitrary path traversal and potential file write/overwrite via `search_id`, `gem_id`, and `local_dir` parameters in FastAPI request schemas.
**Learning:** Raw string inputs used directly with `os.path.join` or format strings for file operations (e.g., `f"prompts/{request.gem_id}.md"`) allow attackers to reference paths outside intended directories unless validated early at the schema level.
**Prevention:** Enforce strict pattern matching (e.g. `^[a-zA-Z0-9_-]+$`) on identifiers and robust path normalization/traversal checks on directory parameters using Pydantic's `field_validator`.
