## 2025-05-15 - [Path Traversal and Input Validation]
**Vulnerability:** User-controlled identifiers (search_id, gem_id) were used directly in file system path construction, allowing for potential directory traversal attacks.
**Learning:** Even with `os.path.join`, if a component is an absolute path or contains `..`, it can escape the intended directory. Pydantic validation is a powerful first line of defense, but `os.path.basename` provides an essential second layer.
**Prevention:** Always use strict regex validation for system identifiers and sanitize path components with `os.path.basename` before use in file operations.
