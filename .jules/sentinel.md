# Sentinel's Journal - Security Critical Learnings

This journal records critical security learnings, vulnerability patterns, and reusable security patterns discovered in this codebase.

---

## 2025-05-22 - Path Traversal in API Endpoints
**Vulnerability:** Path traversal via `gem_id`, `search_id`, and `local_dir` parameters in multiple API endpoints.
**Learning:** Using user-provided strings directly in `os.path.join` or for file operations without strict validation allows accessing or modifying files outside the intended directories (e.g., `prompts/`, `runs/`).
**Prevention:** Centralize identifier validation using a strict regex (e.g., `^[a-zA-Z0-9_-]+$`) and use Pydantic `field_validator` to enforce it at the edge. For path-like inputs like `local_dir`, explicitly block absolute paths and parent directory references (`..`).
