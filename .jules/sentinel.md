## 2026-03-31 - Path Traversal Prevention in Dynamic Prompt Selection
**Vulnerability:** The dynamic prompt refinement endpoint (`/api/v1/gems/refine`) accepted unvalidated `gem_id` values from user input and constructed file paths (`prompts/{gem_id}.md`), creating an arbitrary file read/write path traversal risk.
**Learning:** Dynamic file path construction from user-controlled request parameters without alphanumeric input filtering allows directory traversal sequences (`..`).
**Prevention:** Use Pydantic `@field_validator` with strict regex validation (`re.fullmatch(r"[a-zA-Z0-9_-]+", v)`) to restrict path parameters to trusted character sets before filesystem operations.
