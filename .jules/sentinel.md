## 2026-08-09 - Path Traversal Vulnerabilities in Identifier Inputs

**Vulnerability:** The parameters `search_id`, `candidate_id`, `gem_id`, and `local_dir` in API request schemas (`PipelineRequest`, `SetupSearchRequest`, `RefineRequest`) were utilized to construct file system paths (e.g. `runs/<search_id>/outputs`, `prompts/<gem_id>.md`) without validation. This allowed path traversal using `../` and absolute paths to read or write arbitrary files on the local file system.

**Learning:** When API parameters are directly interpolated into folder structures or filenames, attackers can inject traversal sequences. Generic string parameters in FastAPI Pydantic schemas must be strictly validated or bounded to secure patterns.

**Prevention:** Enforce strict alphanumeric boundaries with regex rules (`^[a-zA-Z0-9_-]+$`) for IDs, and validate relative subdirectory structures by explicitly forbidding double-dots (`..`), absolute prefixes, and drive indicators.
