## 2025-05-22 - Path Traversal Prevention in API Endpoints
**Vulnerability:** User-controlled IDs (`search_id`, `gem_id`, `candidate_id`) and directory paths (`local_dir`) were used directly in `os.path.join` and `open()` calls without sanitization, allowing arbitrary file read/write via directory traversal (e.g., `../../etc/passwd`).
**Learning:** Even with Pydantic for validation, relying on default types like `str` is insufficient for file-system-bound inputs. Explicit regex patterns and `os.path.basename()` provide a robust defense-in-depth approach.
**Prevention:** Always use `Field(pattern=...)` in Pydantic models for any string used in file paths, and apply `os.path.basename()` as a secondary sanitization layer before path construction.
