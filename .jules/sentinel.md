## 2025-05-20 - Enforce strict alphanumeric validation on gem_id in prompt refinement API
**Vulnerability:** Path traversal risk on `/api/v1/gems/refine` where unvalidated `gem_id` string parameter was directly formatted into a file path (`prompts/{request.gem_id}.md`).
**Learning:** `RefineRequest` lacked input validation on `gem_id`. Using `re.fullmatch(r"[a-zA-Z0-9_-]+", v)` in a Pydantic `field_validator` prevents path traversal sequences (`../`, slashes, null bytes) while restricting file access strictly to allowed prompt identifier patterns.
**Prevention:** Always validate path components passed via API requests using strict regex patterns (`re.fullmatch`) or allowlists before passing them to file system operations.
