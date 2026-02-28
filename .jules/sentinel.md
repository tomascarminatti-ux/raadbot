
## 2025-05-14 - Path Traversal in API Identifiers
**Vulnerability:** The 'search_id', 'candidate_id', and 'gem_id' parameters in several API endpoints were used to construct file paths without validation, allowing attackers to create or access files outside the intended directories (e.g., using '../../').
**Learning:** Using raw user input for directory or file names is a high-risk pattern that leads to path traversal. Pydantic models should always enforce strict character allow-lists for such fields.
**Prevention:** Apply regex patterns (e.g., ^[a-zA-Z0-9_-]+$) and length limits to all identifier fields in Pydantic models to ensure they stay within their subdirectories.
