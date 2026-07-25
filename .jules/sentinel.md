# 🛡️ Sentinel's Security Journal - Raadbot v3.0

This journal records critical security learnings, vulnerability patterns, and prevention strategies for the Raadbot ecosystem.

## 2026-03-04 - Unvalidated Identifiers in Path Construction (Path Traversal)
**Vulnerability:** The FastAPI endpoints accepted raw string identifiers (`search_id`, `candidate_id`, `gem_id`) and used them directly to construct file system paths (`runs/{search_id}/outputs`, `prompts/{gem_id}.md`). This allowed potential path traversal (e.g., using `../` sequence) to read, write, or overwrite files outside of the intended directories.
**Learning:** Even internal, non-public APIs must strictly validate all input identifiers. Relying on "internal use only" assumptions creates a weak security posture. Using path construction directly with user-supplied strings can result in remote code execution, sensitive information disclosure, or configuration tampering.
**Prevention:** Implement strict regex-based and whitelist-based Pydantic input validation (`^[a-zA-Z0-9_-]+$`) on all identifier fields. For bounded sets of identifiers (like GEM IDs), enforce exact whitelisting to eliminate any possibility of unauthorized file access.
