## 2025-05-18 - Path Traversal in API Request Handlers
**Vulnerability:** Unvalidated string parameters (`search_id`, `candidate_id`, `gem_id`, `local_dir`) in API request models allowed path traversal attacks (e.g. `../../`) when creating output paths or reading/writing prompt files.
**Learning:** Pydantic request models without strict `field_validator` regex or path checks pass arbitrary string inputs directly into `os.path.join` and open operations, exposing the file system to arbitrary reads and writes.
**Prevention:** Enforce strict alphanumeric-with-dashes/underscores regular expressions (`^[a-zA-Z0-9_-]+$`) on all identifier fields and reject relative traversal sequences (`..`) or absolute path prefixes on file directory parameters using Pydantic field validators.
