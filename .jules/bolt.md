## 2025-05-15 - [Prompt Builder Optimization & Template Recursion]
**Learning:** Moving from sequential `.replace()` calls to a single-pass `re.sub()` significantly improves performance (~9x speedup) but breaks nested variable substitution (e.g., if `{{PROMPT_MAESTRO}}` contains other `{{variables}}`).
**Action:** Use a two-stage construction approach: first resolve the base template (like `{{PROMPT_MAESTRO}}`) using `.replace()`, then resolve all other variables in a single `re.sub` pass to maintain both performance and template recursion.
