## 2026-10-07 - SetupSearchRequest Path Traversal Protection
**Vulnerability:** The `/api/v1/search/setup` endpoint accepted `search_id` parameter without validation and used it directly with `os.path.join("runs", request.search_id, "outputs")`, allowing potential path traversal attacks (e.g., `../../etc`).
**Learning:** Pydantic models handling path-related fields should strictly validate string format using `@field_validator` with `re.fullmatch(r"[a-zA-Z0-9_-]+", v)` to ensure input contains only safe characters and cannot escape intended directories.
**Prevention:** Always enforce strict character set validation on identifiers used in filesystem paths across API request schemas.
