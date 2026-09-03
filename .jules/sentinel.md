## 2025-05-18 - Input Validation and Path Traversal Prevention in FastAPI Models
**Vulnerability:** Unsanitized user inputs in API request payloads (`search_id`, `candidate_id`, `gem_id`, `local_dir`) allowed path traversal vectors (`../`, absolute paths) when constructing filesystem paths (`os.path.join`, prompt file paths).
**Learning:** Standard regex matching (`re.match`) with `$` can allow trailing newline characters (`\n`). Using `re.fullmatch(r"[a-zA-Z0-9_-]+", v)` strictly enforces valid characters across the entire string length without permitting trailing newlines.
**Prevention:** Apply Pydantic `@field_validator` with `re.fullmatch` on all user-supplied identifiers and sanitize/validate path separators (`/`, `\`, `..`) for relative folder path fields.
