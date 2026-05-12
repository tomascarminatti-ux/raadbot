## 2024-05-11 - Pydantic Request Model Hardening
**Vulnerability:** Loose input validation in FastAPI models allowed for potential path traversal and injection via identifier fields and directory paths.
**Learning:** Pydantic v2's `Field(pattern=...)` and `@field_validator` provide a robust, declarative way to enforce security constraints at the entry point, returning 422 Unprocessable Entity automatically before any business logic executes.
**Prevention:** Always use regex patterns for machine-generated IDs and custom validators for any field that interacts with the file system. Use `TestClient(raise_server_exceptions=False)` to verify these error states.
