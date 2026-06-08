## 2025-06-08 - Path Traversal in GEM Refinement
**Vulnerability:** The `/api/v1/gems/refine` endpoint allowed arbitrary file writes by using `gem_id` directly in a file path (e.g., `prompts/{gem_id}.md`) without validation, enabling path traversal (e.g., `gem_id=../../config`).
**Learning:** Even internal-use endpoints for "prompt engineering" need strict whitelisting and input validation when they interact with the filesystem.
**Prevention:** Use a regex pattern for identifiers and a whitelist for sensitive file access.
