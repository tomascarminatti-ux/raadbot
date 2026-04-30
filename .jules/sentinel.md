## 2026-04-30 - Path Traversal Protection via Pydantic
**Vulnerability:** User-provided identifiers (`search_id`, `gem_id`) were interpolated directly into file paths (e.g., `f"prompts/{request.gem_id}.md"`), allowing an attacker to read/write arbitrary files using `..` sequences.
**Learning:** Even if the application logic checks for file existence, an attacker can target existing sensitive files (like `.env` or other prompts) if the identifier isn't strictly validated.
**Prevention:** Use Pydantic's `Field(pattern=...)` to enforce a strict whitelist of safe characters (e.g., `^[a-zA-Z0-9_-]+$`) for all identifiers that touch the file system or database.
