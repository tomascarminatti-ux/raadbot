## 2026-07-22 - Path Traversal in API Requests
**Vulnerability:** Input fields (`search_id`, `candidate_id`, `gem_id`) in several API request models were utilized in constructing file paths (e.g., `os.path.join`, f-strings) without validation, allowing directory/path traversal (e.g., using `../`).
**Learning:** Even internal API endpoints and parameters must strictly validate identifiers using regular expressions to prevent arbitrary file system manipulation, directory creation, or file overwrite/leakage.
**Prevention:** Implement strict input validation on Pydantic request models using `@field_validator` and regular expression matching (e.g., `^[a-zA-Z0-9_-]+$`) to ensure only safe alphanumeric characters with dashes or underscores are accepted.
