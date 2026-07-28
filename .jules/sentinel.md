# Sentinel Security Journal

## 2026-03-01 - Path Traversal Prevention in API Endpoints
**Vulnerability:** Path traversal (directory traversal) and arbitrary file overwrite via unvalidated `search_id`, `candidate_id`, `gem_id`, and `local_dir` input fields in the FastAPI endpoints.
**Learning:** External or user-provided inputs used in file/directory path construction (e.g., in `os.path.join` or file openings) must be explicitly sanitized and validated. Without validation, attackers can use traversal sequences like `../` to access, read, or overwrite files anywhere on the container's filesystem.
**Prevention:** Implement strict Pydantic `field_validator` regex validations (e.g., `^[a-zA-Z0-9_-]+$`) for IDs, and forbid directory traversal elements (like `..`) and root/absolute path structures for relative directories, ensuring all parameters are securely constrained before interacting with file system APIs.
