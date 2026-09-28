## 2026-03-30 - Path Traversal Vulnerability in GEM Refinement API
**Vulnerability:** Unsanitized `gem_id` field in `RefineRequest` permitted relative file path traversal (e.g. `../` or `../../`), potentially writing prompt files outside the intended `prompts/` directory.
**Learning:** `re.match` with `$` allows trailing newlines (`\n`). Using `re.fullmatch(r"[a-zA-Z0-9_-]+", v)` strictly ensures input is strictly alphanumeric, underscore, or hyphen without trailing newline characters.
**Prevention:** Always use `@field_validator` with strict `re.fullmatch` regex checks for any identifier field incorporated into file paths.
