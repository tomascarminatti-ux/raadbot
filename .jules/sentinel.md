# 🛡️ Sentinel's Security Journal

## 2026-08-14 - Directory Traversal and Input Validation Vulnerabilities in API Request Schemas
**Vulnerability:** The API endpoints (`/api/v1/run`, `/api/v1/search/setup`, and `/api/v1/gems/refine`) parsed request bodies using Pydantic models but lacked validation on identifier fields (`search_id`, `candidate_id`, `gem_id`) and directory fields (`local_dir`). This allowed directory traversal payloads (e.g., `../`, `..\\`) and arbitrary file reading/writing/execution because user-supplied input was directly interpolated into filesystem paths.

**Learning:** Relying solely on Pydantic's default types (like `str`) without adding specific regular expression matches or format constraints leaves path-building logic vulnerable to directory traversal. Path normalization (such as replacing `\\` with `/`) must be performed prior to any containment checks (like looking for `..`) to prevent OS-specific path bypasses.

**Prevention:** Always define strict regular expression constraints (e.g., `^[a-zA-Z0-9_-]+$`) on identifiers that compose file names or directory paths. For directory inputs, normalize backslashes and strictly block `..`, absolute paths, or device letters. Enforce allowlists where the set of valid identifiers is known (e.g., limiting `gem_id` strictly to `["gem1", "gem2", "gem3", "gem4", "gem5"]`).
