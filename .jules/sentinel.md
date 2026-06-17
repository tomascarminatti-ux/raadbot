## 2025-05-15 - Path Traversal in GEM Refinement
**Vulnerability:** The `/api/v1/gems/refine` endpoint accepted arbitrary `gem_id` strings, which were used to construct file paths (e.g., `f"prompts/{request.gem_id}.md"`). This allowed reading/overwriting any file on the system that the application had permissions to access by using sequences like `../`.
**Learning:** Appending a hardcoded file extension (like `.md`) is not a sufficient defense against path traversal, as attackers can still navigate upwards in the directory tree or target other files with that extension.
**Prevention:** Always validate user-provided identifiers against a strict regex pattern (e.g., `^[a-zA-Z0-9_-]+$`) and use an explicit whitelist for critical file operations.
