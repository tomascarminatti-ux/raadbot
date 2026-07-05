## 2025-05-22 - Path Traversal in Multi-Agent Pipeline API
**Vulnerability:** API endpoints (`/api/v1/run`, `/api/v1/search/setup`, `/api/v1/gems/refine`) were vulnerable to path traversal via `search_id`, `local_dir`, and `gem_id` parameters.
**Learning:** Using user-provided strings directly in `os.path.join` or `open()` without strict validation allows attackers to read/write files outside intended directories (e.g., `runs/`, `prompts/`).
**Prevention:** Enforce strict alphanumeric patterns for identifiers using Pydantic `Field(pattern=...)` and use `@field_validator` to reject absolute paths or directory navigation (`..`) in path parameters.
