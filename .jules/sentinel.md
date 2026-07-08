## 2025-05-15 - [Path Traversal Prevention via ID Validation]
**Vulnerability:** Path traversal vulnerabilities were identified in endpoints accepting `search_id`, `gem_id`, and `local_dir`. An attacker could use `..` to access or modify files outside the intended directories.
**Learning:** Whitelist-based validation using regex (`^[a-zA-Z0-9_-]+$`) is a simple and effective first line of defense for identifiers that map to file system components.
**Prevention:** Always validate identifiers against a strict pattern and use `os.path.abspath` with prefix checking for any user-provided path components.
