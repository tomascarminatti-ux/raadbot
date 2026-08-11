# Sentinel's Security Journal

## 2026-08-11 - Path Traversal Vulnerability in GEM API Endpoints
**Vulnerability:** The parameters `search_id`, `candidate_id`, and `gem_id` were accepted from the user without validation and joined into filesystem paths, allowing arbitrary directory traversal sequences (such as `../`) to access or modify arbitrary files on the system (Arbitrary File Read/Write).
**Learning:** Raw input strings used in file paths or configurations must always be strictly validated against alphanumeric character limits to prevent path manipulation.
**Prevention:** Enforce rigorous Pydantic `field_validator` regex validations (`^[a-zA-Z0-9_-]+$`) or whitelists on any string parameters used in local path construction.
