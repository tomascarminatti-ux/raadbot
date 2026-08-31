## 2025-08-31 - Input Sanitization & Path Traversal Validation in API Request Models

**Vulnerability:** API payload models (`PipelineRequest`, `SetupSearchRequest`, `RefineRequest`) accepted unvalidated string inputs for `search_id`, `candidate_id`, `gem_id`, and `local_dir`, allowing directory traversal vectors (e.g. `../`) or arbitrary file path manipulation when loading or writing local runs/prompts.
**Learning:** Pydantic models in FastAPI applications require strict regex validation (`re.fullmatch(r"[a-zA-Z0-9_-]+", v)`) for identifiers and explicit backslash-to-forward-slash path normalization before checking for path traversal (`..` components or absolute path prefixes).
**Prevention:** Always apply `@field_validator` hooks on user-supplied identifier and file path parameters in Pydantic models to restrict allowable character sets and enforce path isolation.
