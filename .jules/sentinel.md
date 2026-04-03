## 2025-05-22 - Defense in Depth for Path Traversal
**Vulnerability:** Path traversal via user-controlled IDs (search_id, gem_id, candidate_id) and `local_dir` used in file paths.
**Learning:** Regex validation (`^[a-zA-Z0-9_-]+$`) in Pydantic models is the first line of defense. `os.path.basename()` provides a secondary layer in case validation is bypassed or misconfigured in future updates. For `local_dir`, allowing dots while blocking `..` is necessary for supporting versioned directories.
**Prevention:** Combine input validation (strict regex and `..` blocking) with path sanitization (`os.path.basename`) before using user input in `os.path.join` or file operations.
