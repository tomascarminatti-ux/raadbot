## 2025-05-14 - Input Validation and Path Traversal Protection
**Vulnerability:** Lack of input validation in `api.py` endpoints allowed potential path traversal via `local_dir` and `gem_id`, and potential identifier injection via `search_id`.
**Learning:** FastAPI's reliance on Pydantic models for request parsing provides a centralized place for security guardrails. Using `Field(pattern=...)` and `@field_validator` can effectively block malicious payloads before they reach application logic.
**Prevention:** Always use regex patterns for identifiers and explicitly validate path-like inputs to block `..` and absolute paths.
