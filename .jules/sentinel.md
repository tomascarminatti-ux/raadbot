## 2025-05-14 - API Identifier and Path Hardening
**Vulnerability:** Lack of strict validation on user-provided identifiers (search_id, gem_id, etc.) and file paths (local_dir) in FastAPI endpoints. This could lead to Path Traversal if identifiers are used in file operations or SQL Injection if used in raw queries.
**Learning:** Pydantic models are the first line of defense in FastAPI. Using `Field(pattern=...)` and `@field_validator` allows for centralized, declarative security constraints that are automatically enforced by the framework.
**Prevention:** Always restrict identifiers to a safe character set (e.g., `^[a-zA-Z0-9_-]+$`) and explicitly reject absolute paths or parent directory references (`..`) in fields that represent local filesystem locations.
