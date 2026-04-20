## 2025-05-15 - [Path Traversal in API Request Models]
**Vulnerability:** Input fields (`search_id`, `gem_id`, `candidate_id`) were used directly in `os.path.join` to construct file paths for reading/writing prompts and run outputs. An attacker could use `..` sequences or absolute paths to read or overwrite files outside the intended directories (e.g., `search_id="../../etc/passwd"`).
**Learning:** Pydantic's default `str` type does not perform any path-safety validation. Even when using `os.path.join`, Python returns an absolute path if any component is absolute, bypassing the intended root directory.
**Prevention:** Use strict regex patterns (`Field(pattern=...)`) for identifiers and custom `@field_validator` to explicitly block `..`, `/`, and `\` in any user-provided path components.
