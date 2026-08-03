# Sentinel Security Journal

## 2026-08-03 - Path Traversal Vulnerability in FastAPI Prompt Refinement and Run Endpoints
**Vulnerability:** Input fields including `gem_id`, `search_id`, and `local_dir` were passed directly to filesystem operations (like `open()` and `os.makedirs()`) without validation. This allowed attackers to perform path traversal using `../` sequences, leading to arbitrary file read/write (via prompt refinement) and arbitrary directory scanning/creation (via run setup).
**Learning:** Pydantic models acting as request schemas should validate and sanitize inputs at the system's boundary. Restricting identifiers to strict character sets and normalizing slash representations in relative path inputs prevent attackers from escaping designated sandbox directories.
**Prevention:** Always declare Pydantic `field_validator` decorators to enforce strict ID patterns (disallowing `/`, `\`, and `..`) and ensure that relative directory parameters do not start with a root separator, contain drive letters, or utilize traversal components.
