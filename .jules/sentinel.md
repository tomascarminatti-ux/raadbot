## 2025-05-23 - Path Traversal & Input Validation
**Vulnerability:** Path Traversal via unvalidated identifiers (`search_id`, `gem_id`) used in file path construction.
**Learning:** Request models using `str` without constraints are susceptible to path manipulation (e.g., `../../etc/passwd`). Testing security fixes requires careful mocking to avoid side effects like overwriting source files (as seen with `prompts/gem1.md`).
**Prevention:** Use Pydantic `@field_validator` with a centralized regex (`config.ID_PATTERN`) for all identifier-like fields. Ensure tests use `mocker.mock_open` or temporary directories when interacting with the filesystem.
