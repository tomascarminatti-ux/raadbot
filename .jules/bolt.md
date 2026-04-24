## 2025-05-15 - [Prompt Builder Optimization]
**Learning:** In `agent/prompt_builder.py`, `{{PROMPT_MAESTRO}}` must be injected before the final variable substitution pass to ensure variables within the maestro template are correctly expanded. Single-pass substitution with `re.sub` is significantly faster than multiple `.replace()` calls.
**Action:** Always inject composite templates before leaf variables when using single-pass substitution.
