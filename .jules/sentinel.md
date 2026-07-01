## 2025-05-22 - Path Traversal Protection via Pydantic Validation
**Vulnerability:** Path Traversal in API endpoints accepting file system identifiers (`search_id`, `gem_id`, `local_dir`).
**Learning:** `os.path.join` on Unix/Linux systems treats an absolute path as a new root, ignoring previous components. This allows identifiers to escape the intended base directory (e.g., `runs/` or `prompts/`) if they start with `/` or contain `..`.
**Prevention:** Enforce strict alphanumeric regex patterns on identifiers using Pydantic's `Field(pattern=...)` and use `@field_validator` to reject absolute paths or `..` components in directory strings.
