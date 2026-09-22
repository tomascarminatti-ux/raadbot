# Sentinel Security Journal

## 2025-05-20 - Input Validation and Path Traversal Prevention in API Models
**Vulnerability:** API request models (`PipelineRequest`, `SetupSearchRequest`, `RefineRequest`) accepted unvalidated string inputs for file/folder identifiers (`search_id`, `candidate_id`, `gem_id`) and local directory paths (`local_dir`). These values were passed directly into `os.path.join()` or file open operations, creating potential directory traversal and arbitrary path construct risks.
**Learning:** Pydantic models without strict field validators allow path control characters like `..`, `/`, and backslashes `\`. When endpoints read or write local files based on API payloads, identifier parameters must be sanitized at the API request level before reaching underlying handlers.
**Prevention:** Use Pydantic `@field_validator` hooks with `re.fullmatch(r"[a-zA-Z0-9_-]+", v)` for identifiers and block relative traversal tokens (`..`) or absolute path prefixes on local filesystem parameters.
