# Sentinel Security Journal

## 2026-03-01 - Path Traversal Vulnerability via API Request Fields
**Vulnerability:** User-controlled request fields (`search_id`, `gem_id`, `candidate_id`, `local_dir`) were accepted without restriction. This enabled path traversal attacks (such as `../`) to manipulate files outside of the intended directories or read/write arbitrary configuration/source files.
**Learning:** Relying solely on downstream loaders or path handlers for security is insufficient. The API gateway (FastAPI/Pydantic) must enforce strict type/pattern boundaries as the first line of defense before parameters propagate to storage systems, file streams, or orchestration logic.
**Prevention:** Always leverage Pydantic's V2 `@field_validator` on any file-system-bound fields (such as directory or file IDs) to enforce restrictive alphanumeric-only regex patterns (`^[a-zA-Z0-9_-]+$`) and to actively filter out traversal parts (`..`) and absolute paths.
