## 2025-05-18 - Strict Regex Match vs End Anchor in Pydantic Validation
**Vulnerability:** Path traversal and command/parameter injection via identifier fields in FastAPI request bodies (`search_id`, `candidate_id`, `gem_id`).
**Learning:** Using `re.match(r"[a-zA-Z0-9_-]+$", v)` allows trailing newlines (`\n`) because `$` matches before a newline at the end of the string.
**Prevention:** Always use `re.fullmatch(r"[a-zA-Z0-9_-]+", v)` when validating strings in Pydantic field validators to ensure complete match without newline bypasses.
