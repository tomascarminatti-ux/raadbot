## 2025-04-25 - Identifier Path Traversal Hardening
**Vulnerability:** Path Traversal via unvalidated identifiers in API requests.
**Learning:** Identifier fields like `search_id` or `gem_id` that are used to construct file system paths (e.g., `os.path.join("runs", search_id)`) or template paths (e.g., `f"prompts/{gem_id}.md"`) are high-risk entry points for path traversal attacks if they allow characters like `..`, `/`, or `\`.
**Prevention:** Always apply strict whitelist validation to such identifiers. A regex pattern like `^[a-zA-Z0-9_-]+$` ensures only safe characters are allowed, effectively neutralizing traversal attempts at the validation layer.
