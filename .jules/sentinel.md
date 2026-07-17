# Sentinel Security Journal

This journal records critical security-related learnings, vulnerabilities, and prevention patterns discovered in this codebase.

## 2025-06-18 - Input Validation and Path Traversal Prevention in API Endpoints
**Vulnerability:** Path Traversal via unvalidated `search_id`, `candidate_id`, and `gem_id` fields in API endpoints.
**Learning:** Endpoints that construct file paths dynamically using user-supplied identifiers (such as `search_id` or `gem_id`) are vulnerable to directory traversal (e.g. using `../`) if input is not strictly validated against a strict character whitelist.
**Prevention:** Use Pydantic field validators to strictly validate identifiers against a safe regex whitelist (`r'^[a-zA-Z0-9_-]+$'`) to ensure they cannot contain directory traversal sequences or other dangerous characters.
