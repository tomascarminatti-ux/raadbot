# Sentinel's Security Journal

## 2025-05-18 - Path Traversal In Validation via Pydantic Field Validators
**Vulnerability:** API endpoints (`/api/v1/run`, `/api/v1/search/setup`, `/api/v1/gems/refine`) accepted string identifiers (`search_id`, `candidate_id`, `gem_id`) and relative file paths (`local_dir`) without validation, allowing directory traversal sequences (such as `..` or absolute paths) that could read or overwrite arbitrary filesystem files outside intended `runs/` or `prompts/` directories.
**Learning:** Unvalidated string fields passed directly to file path construction operations (`os.path.join` or format strings) in FastAPI endpoint schemas can bypass intended folder scoping unless sanitized at the entry point schema layer.
**Prevention:** Enforce strict alphanumeric regex validation (`re.fullmatch(r"[a-zA-Z0-9_-]+", v)`) on identifier fields and sanitize directory paths against `..` traversals and absolute prefixes using Pydantic `field_validator` on API request models.
