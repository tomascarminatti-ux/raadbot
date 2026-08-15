## 2026-08-15 - Input Validation to Prevent Path Traversal in File Operations

**Vulnerability:** User-supplied API path parameters (`search_id`, `gem_id`, `candidate_id`, `local_dir`) were concatenated directly into filesystem operations (`os.path.join("runs", search_id)`, `f"prompts/{gem_id}.md"`) without input sanitization or path traversal validation.
**Learning:** FastApi models using default Pydantic `str` types do not enforce path boundaries. Attacker payloads containing relative directory traversal elements (such as `../`) could traverse outside intended root directories when interacting with filesystem endpoints.
**Prevention:** Always attach Pydantic `@field_validator` on model fields that participate in file path construction. Enforce strict alphanumeric regex (`^[a-zA-Z0-9_-]+$`) for IDs and disallow `..` path sequences, leading slashes, and Windows drive prefixes on path fields.
