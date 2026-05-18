## 2025-05-24 - Identifier Validation and Error Masking
**Vulnerability:** Input validation bypass and information leakage.
**Learning:** Endpoints using `Dict[str, Any]` for input skip Pydantic's validation. Raw exception messages in `HTTPException` can leak database schema details.
**Prevention:** Always use structured Pydantic models with `Field(pattern=...)` for identifiers and mask database errors with generic messages.
