## 2025-05-14 - [Path Traversal in Pydantic Models]
**Vulnerability:** Lack of regex validation on identifier fields (`search_id`, `entity_id`) used in filesystem paths and SQL queries allowed path traversal (e.g., `../`).
**Learning:** Default Pydantic `str` types are permissive. For fields used in path construction, explicit regex patterns or path sanitizers are necessary.
**Prevention:** Use `Field(pattern=r"^[a-zA-Z0-9_-]+$")` for all identifiers and custom validators for directory paths.
