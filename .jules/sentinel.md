## 2025-05-22 - Path Traversal and Information Leakage Prevention
**Vulnerability:** API endpoints used user-provided identifiers (search_id, gem_id) directly in file paths and returned raw exception messages.
**Learning:** Lack of input validation on identifiers used for filesystem operations created path traversal risks, and verbose error messages could leak system internals.
**Prevention:** Enforce strict alphanumeric regex patterns for identifiers in Pydantic models, use whitelisting for file access, and return generic error messages for internal failures.
