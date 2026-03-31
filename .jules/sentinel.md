## 2025-05-15 - [Path Traversal in API Endpoints]
**Vulnerability:** User-controlled IDs (`search_id`, `gem_id`, `candidate_id`) and directory paths (`local_dir`) were used directly in file system operations without validation or sanitization, allowing for arbitrary file read/write outside intended directories.
**Learning:** Pydantic models are a powerful first line of defense for input validation. Combined with defensive programming like `os.path.basename()`, they provide defense-in-depth against path traversal.
**Prevention:** Always validate user-provided strings that will be used as part of a file path. Use strict regex patterns in Pydantic and apply path normalization/sanitization at the point of use.
