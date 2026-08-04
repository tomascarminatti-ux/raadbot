# Sentinel's Journal: Security Learnings

## 2026-08-04 - FastAPI Input Path Traversal Vulnerability
**Vulnerability:** Endpoints handling file system paths or identifiers (e.g., `search_id`, `gem_id`, `candidate_id`, `local_dir`) dynamically joined those strings using `os.path.join` or format strings (e.g., `prompts/{request.gem_id}.md`) without performing prior character or path sanitization. An attacker could supply directory traversal sequences like `../` to access, read, or overwrite arbitrary files on the system host.
**Learning:** Even when inputs are loaded into a well-defined Pydantic data model, they remain raw strings from untrusted clients unless strict validation constraints (e.g., `field_validator`, regex patterns, or allowed lists) are explicitly configured on the Pydantic class fields.
**Prevention:** Always restrict identifiers utilized in filesystem structures to safe characters (such as alphanumeric, hyphens, and underscores) via regex match checks, and explicitly filter out traversal sequences like `..`, colons, or root slashes from paths such as `local_dir`.
