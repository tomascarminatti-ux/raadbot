## 2025-05-15 - [Path Traversal in API Identifiers]
**Vulnerability:** User-provided identifiers (`search_id`, `gem_id`, `candidate_id`) were used directly in `os.path.join` or f-strings to construct file paths, allowing directory traversal (e.g., `search_id="/etc/passwd"` resulting in `/etc/passwd`).
**Learning:** In Python, `os.path.join(base, user_input)` is vulnerable if `user_input` is an absolute path, as it will ignore `base`. Even relative traversal (`../`) can escape intended directories.
**Prevention:** Strictly validate all identifier-like inputs using regex (e.g., `r"^[a-zA-Z0-9_-]+$"`) via Pydantic `Field(pattern=...)` to ensure they only contain safe characters.
