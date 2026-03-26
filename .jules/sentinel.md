## 2025-05-15 - [Path Traversal in API Endpoints]
**Vulnerability:** Several API endpoints (`/run`, `/search/setup`, `/gems/refine`) used user-provided ID strings to construct file system paths without proper sanitization.
**Learning:** Pydantic models provided a first layer of defense via regex patterns, but manual path manipulation in the logic (e.g., using `os.path.join` with unsanitized inputs) still posed a risk if validation was bypassable or insufficiently strict.
**Prevention:** Use a combination of Pydantic `Field(pattern=...)` for strict input validation and `os.path.basename()` as a defense-in-depth measure before any file system operation involving user-controlled strings.
