# Sentinel Security Journal

## 2026-03-30 - Pydantic Field Validator Regex End-of-String Matching
**Vulnerability:** Path traversal risks via unsanitized identifiers (`search_id`, `gem_id`, `candidate_id`) and directory traversal in `local_dir` in API request payloads.
**Learning:** In Python regex, `re.match(r"^[a-zA-Z0-9_-]+$", v)` accepts trailing newlines (`\n`) because `$` matches before a final newline.
**Prevention:** Use `re.fullmatch(r"[a-zA-Z0-9_-]+", v)` for strict input validation in Pydantic field validators.
