## 2026-02-25 - API Hardening and Secret Management
**Vulnerability:** Path traversal via `local_dir` and `gem_id` parameters, and hardcoded/tracked `.env` file.
**Learning:** Pydantic models without explicit validation patterns are susceptible to injection and traversal. Tracked `.env` files even if in `.gitignore` remain in the history and index.
**Prevention:** Use Pydantic `Field(pattern=...)` for identifiers and `@field_validator` for path safety. Ensure `.env` is removed from git index (`git rm --cached`).
