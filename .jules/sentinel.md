## 2025-05-15 - Path Traversal in GEM endpoints
**Vulnerability:** Path traversal via search_id and gem_id in /api/v1/run, /api/v1/search/setup, and /api/v1/gems/refine.
**Learning:** User-provided IDs used in file paths were not sanitized or validated, allowing access to files outside intended directories (e.g., prompts/).
**Prevention:** Use Pydantic Field patterns to restrict IDs to safe characters (^[a-zA-Z0-9_-]+$) and apply os.path.basename() as defense-in-depth before path construction.
