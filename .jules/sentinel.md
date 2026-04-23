## 2025-05-15 - [Path Traversal & Injection Prevention via Pydantic]
**Vulnerability:** Identifiers (search_id, entity_id) were used directly in filesystem paths and database queries without validation. Additionally, directory paths were accepted without checking for traversal sequences (..).
**Learning:** The application relied on manual folder creation and SQLite queries using user-provided strings, making it vulnerable to path traversal and potential command/SQL injection if these strings contained malicious characters.
**Prevention:** Always harden Pydantic models with `Field(pattern=r"^[a-zA-Z0-9_-]+$")` for identifiers and use custom `@field_validator` to block absolute paths and ".." in directory fields.
