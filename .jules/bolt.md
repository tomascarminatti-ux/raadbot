# Bolt's Performance Journal

## 2025-05-15 - [Optimization of Pipeline Hot-paths]
**Learning:** Using `jsonschema.validate` directly is significantly slower (~60x) than pre-compiling a validator instance with `validator_for(schema)(schema)` because it avoids re-validating the schema itself against the meta-schema on every call. Additionally, in `agent/prompt_builder.py`, `{{PROMPT_MAESTRO}}` must be injected *before* the single-pass regex substitution to ensure that any variable placeholders within the maestro template itself are properly resolved.
**Action:** Always pre-compile JSON validators if used in loops or frequent request paths. Use a two-step approach for nested template injection (inject base template first, then replace all variables in one pass).
