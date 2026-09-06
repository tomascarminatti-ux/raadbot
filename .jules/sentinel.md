## 2026-03-30 - Path Traversal Prevention in API Request Models
**Vulnerability:** Unvalidated request parameters (`search_id`, `candidate_id`, `gem_id`, `local_dir`) in API models were directly formatted or joined into filesystem path operations (`os.path.join`, `prompts/{gem_id}.md`), allowing potential directory traversal attacks.
**Learning:** API request payloads using Pydantic models must validate string fields before passing them to file path constructs, especially when default parameter fields map to server-side directories.
**Prevention:** Enforce strict regex validation (`^[a-zA-Z0-9_-]+$`) on identifier fields and reject traversal sequences (`..`), absolute path prefixes, or drive letters in directory paths using Pydantic `@field_validator`.
