## 2025-05-15 - Path Traversal in GEM Refinement and Search Setup
**Vulnerability:** User-controlled identifiers (gem_id, search_id) were used to construct file paths without validation, allowing directory traversal (e.g., ../../etc/passwd) when combined with file extensions.
**Learning:** Even if an extension is appended (.md), path traversal can still occur if the ID contains ".." sequences. Pydantic's regex validation is an effective first line of defense.
**Prevention:** Always use strict regex validation for user-provided identifiers and apply `os.path.basename()` as a defense-in-depth measure before using identifiers in file system operations.
