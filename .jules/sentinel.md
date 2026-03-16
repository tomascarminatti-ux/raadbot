## 2025-05-15 - [Path Traversal and Input Validation]
**Vulnerability:** Path traversal via `search_id` and `local_dir` in API requests, and potential identifier injection in database API.
**Learning:** Using `os.path.join` with unsanitized user input allows attackers to escape intended directories if the input contains `..` or is an absolute path. Restricting identifiers to alphanumeric/slug patterns at the Pydantic model level effectively mitigates these risks before they reach the logic layer.
**Prevention:** Apply strict regex patterns to all identifier fields and use custom validators for any path-like inputs to reject traversal sequences and absolute paths.
