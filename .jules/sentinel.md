## 2025-05-15 - [Critical] Path Traversal and Information Leakage in API
**Vulnerability:** API endpoints allowed path traversal via `search_id`, `gem_id`, and `local_dir` parameters. Additionally, detailed exception messages were leaked in error responses.
**Learning:** Using unsanitized user input directly in `os.path.join` or file path strings without strict validation or normalization leads to traversal risks. Returning `str(e)` in `HTTPException` can expose sensitive internal paths and logic.
**Prevention:** Enforce strict alphanumeric/slug patterns on IDs using Pydantic validators. Use `os.path.abspath` and verify the resolved path starts with the expected base directory. Always return generic, localized error messages to users while logging details internally.
