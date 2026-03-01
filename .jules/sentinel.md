## 2024-05-22 - Path Traversal Prevention in API Inputs
**Vulnerability:** Path traversal via search_id, local_dir, and gem_id fields in API requests.
**Learning:** Using identifiers directly in file system paths without validation allows attackers to read or write files outside intended directories (e.g., using `../`).
**Prevention:** Apply strict Pydantic `Field` patterns (regex) for identifiers and use `@field_validator` to block '..' sequences in directory paths. Ensure absolute paths are blocked by checking for leading slashes.
