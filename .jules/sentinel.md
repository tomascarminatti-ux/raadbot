## 2025-05-14 - Path Traversal in API Endpoints
**Vulnerability:** API endpoints accepted unvalidated strings for search IDs and local directories, which were used directly in file system operations (os.path.join, os.makedirs, open).
**Learning:** Even internal APIs should strictly validate input patterns for identifiers used in paths to prevent directory traversal and unauthorized file access.
**Prevention:** Use Pydantic's `Field(pattern=...)` to restrict identifier characters and validate path structures.
