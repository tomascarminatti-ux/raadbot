## 2025-06-03 - Path Traversal in GEM Refinement
**Vulnerability:** Path traversal via `gem_id` and `search_id` in API endpoints.
**Learning:** Unsanitized user input was directly used to construct file system paths (e.g., `prompts/{gem_id}.md`), allowing potential access to arbitrary files.
**Prevention:** Enforce strict regex validation for identifiers (`r'^[a-zA-Z0-9_-]+$'`) using Pydantic models and implement an explicit whitelist for identifiers that map to the filesystem.
