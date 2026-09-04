## 2025-05-20 - API Request Path Traversal Prevention
**Vulnerability:** Unsanitized user inputs (`search_id`, `candidate_id`, `gem_id`, `local_dir`) in API request models allowed arbitrary file system path traversal (`../`) when building output directories or loading template files.
**Learning:** Pydantic models in FastAPI endpoints can accept arbitrary relative/absolute paths unless restricted by custom field validators. Using `re.match` with `$` alone can allow trailing newlines (`\n`).
**Prevention:** Use `re.fullmatch(r"[a-zA-Z0-9_-]+", v)` for strict alphanumeric identifier validation and normalize backslashes (`\`) to forward slashes (`/`) before checking for directory traversal sequences (`..`) in relative path inputs.
