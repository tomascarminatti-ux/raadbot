## 2025-04-16 - Path Traversal Prevention via Pydantic Regex Validation
**Vulnerability:** Unvalidated identifiers (`search_id`, `gem_id`, `candidate_id`) were used directly in `os.path.join` and file path construction, allowing path traversal (e.g., using `..` to access or create files outside intended directories).
**Learning:** Pydantic's `Field(pattern=...)` provides a declarative and robust way to enforce strict character sets at the API gateway level, preventing common injection and traversal attacks before they reach business logic.
**Prevention:** Always use strict regex patterns (e.g., `r"^[a-zA-Z0-9_-]+$"`) for any identifier that will be used in filesystem operations or database queries.
