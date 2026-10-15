# Sentinel Security Journal

## 2025-05-18 - Path Traversal Prevention in API Endpoints
**Vulnerability:** API request endpoints (`/api/v1/run`, `/api/v1/search/setup`, `/api/v1/gems/refine`) accepted unvalidated string parameters (`search_id`, `candidate_id`, `gem_id`, `local_dir`) that were used directly in `os.path.join` and file write operations without path sanitization.
**Learning:** Pydantic models with plain `str` type annotations allow arbitrary user input including relative traversal sequences (`../`), absolute paths (`/etc/passwd`), and Windows path structures (`C:\`).
**Prevention:** Enforce strict regular expression validation (`re.fullmatch(r"[a-zA-Z0-9_-]+", v)`) on string identifiers and reject path traversal sequences (`..`, absolute prefixes, drive letters) using Pydantic `field_validator`.
