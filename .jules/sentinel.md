## 2025-05-15 - Path Traversal in GEM Identifiers
**Vulnerability:** Path traversal via `search_id`, `gem_id`, and `local_dir` parameters used in file system operations.
**Learning:** Default Pydantic `str` fields allow special characters like `.` and `/` which, when passed to `os.path.join`, can lead to directory escape. This was present in multiple orchestrator and refinement endpoints.
**Prevention:** Enforce strict regex patterns (`^[a-zA-Z0-9_-]+$`) for all identifier fields and use `os.path.abspath` prefix verification for any path-like inputs.
