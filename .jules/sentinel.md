## 2025-05-15 - Identifier Hardening and Path Traversal Prevention
**Vulnerability:** API endpoints and DB API models accepted arbitrary strings for identifier fields (like `search_id`, `entity_id`) and path fields (like `local_dir`), enabling potential path traversal attacks and file system manipulation.
**Learning:** Pydantic models without explicit validation patterns allow any string, which can be dangerous when those strings are later used in file system operations (e.g., `os.path.join("runs", search_id, ...)`).
**Prevention:** Use `Field(pattern=r"^[a-zA-Z0-9_-]+$")` to strictly limit identifiers to a safe set of characters. For path fields, use `@field_validator` to explicitly block ".." and absolute paths if they are intended to be relative and scoped.

## 2025-05-15 - CI Remediation: Submodule Gitlink Removal
**Vulnerability:** The repository contained a broken gitlink to `zeroclaw` without a corresponding `.gitmodules` entry, causing CI failures with exit code 128 during git operations.
**Learning:** Broken gitlinks (submodules without metadata) can bottleneck CI pipelines and prevent automated security checks from running.
**Prevention:** Always ensure `.gitmodules` is consistent with the index or remove unused gitlinks using `git rm --cached <path>` to maintain repository integrity.
