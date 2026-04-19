## 2025-05-15 - [Path Traversal in os.path.join]
**Vulnerability:** Use of `os.path.join` with unsanitized user input allowed for arbitrary file system access (path traversal).
**Learning:** In Python, `os.path.join('base', '/absolute/path')` returns `'/absolute/path'`, completely ignoring the base directory. This is a common pitfall when developers assume `os.path.join` always produces a path relative to the first argument.
**Prevention:** Strictly validate user-provided identifiers using regex (e.g., `^[a-zA-Z0-9_-]+$`) to ensure they do not contain leading slashes, `..`, or other path-modifying characters before passing them to `os.path.join`.
