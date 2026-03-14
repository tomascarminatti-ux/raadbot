## 2025-05-15 - Path Traversal via Identifier Fields
**Vulnerability:** User-controlled identifier fields (`search_id`, `gem_id`, etc.) were used directly in `os.path.join` and `os.makedirs` without sanitization, allowing an attacker to create directories or read/write files outside the intended scope (e.g., `search_id="../evil_dir"`).
**Learning:** In Python, `os.path.join` does not prevent path traversal if a component is an absolute path or contains `..` segments. Even when prepending a "safe" base directory, an attacker can "escape" it.
**Prevention:** Use Pydantic's `Field(pattern=...)` to strictly limit identifiers to alphanumeric characters, underscores, and hyphens. Additionally, explicitly validate path-like inputs to reject `..` and leading slashes.
