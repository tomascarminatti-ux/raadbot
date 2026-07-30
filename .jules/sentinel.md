# Sentinel's Journal - Critical Learnings Only

## 2026-07-30 - Identifier-based Path Traversal Vulnerabilities
**Vulnerability:** Path traversal in file-system operations where user-supplied IDs (such as `search_id`, `candidate_id`, or `gem_id`) are concatenated directly into local directory paths (e.g., `prompts/{gem_id}.md` or `runs/{search_id}/outputs`) without validation. This allowed reading/writing of arbitrary files.
**Learning:** Standard validation libraries like Pydantic can be leverage directly within the request schema definition via `@field_validator` to reject traversal characters (`..`, `/`, `\`) early, before any file-system APIs are invoked.
**Prevention:** Always restrict identifiers to a safe alphanumeric format (`^[a-zA-Z0-9_-]+$`) in endpoint request definitions, and ensure `local_dir` values block relative directory traversal parts (`..`) and absolute path indicator prefixes.
