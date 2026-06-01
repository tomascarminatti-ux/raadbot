## 2025-05-24 - Path Traversal in GEM Refinement
**Vulnerability:** Path traversal in `/api/v1/gems/refine` via unvalidated `gem_id` parameter.
**Learning:** Using user-provided strings directly in file paths (e.g., `f"prompts/{request.gem_id}.md"`) without sanitization or whitelisting allows access to files outside the intended directory.
**Prevention:** Implement strict whitelisting for resource identifiers and use Pydantic `Field(pattern=...)` for alphanumeric validation of IDs used in filesystem operations.

## 2025-05-24 - Information Leakage via raw Exceptions
**Vulnerability:** API endpoints and webhooks were returning `str(e)` in error responses.
**Learning:** Returning raw exception messages can leak sensitive internal details, such as file paths, database schemas, or logic errors, to potential attackers.
**Prevention:** Mask raw exceptions in production API responses with generic error messages and log the actual details internally.
