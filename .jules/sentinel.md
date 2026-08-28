## 2026-02-25 - Path Traversal In Validation Requests
**Vulnerability:** API endpoints (`/api/v1/run`, `/api/v1/search/setup`, `/api/v1/gems/refine`) relied on unvalidated string inputs for file paths and directory outputs (`search_id`, `candidate_id`, `local_dir`, `gem_id`), creating path traversal risks.
**Learning:** Pydantic models require explicit regex validators using `re.fullmatch(r"[a-zA-Z0-9_-]+", v)` on identifiers and relative directory normalization to ensure safe filesystem interaction.
**Prevention:** Always validate all path parameters and identifiers in API Pydantic models using regex or traversal checks before passing them to `os.path.join` or open file operations.
