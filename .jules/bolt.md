# Bolt's Performance Journal

## 2025-05-15 - [JSON Schema Validation & Prompt Building]
**Learning:** `jsonschema.validate` re-parses the schema on every call, causing significant overhead (~2.3ms per call). Pre-compiling the validator using `jsonschema.validators.validator_for` reduces this to ~40µs (a ~58x speedup). Additionally, `build_prompt` was a minor bottleneck (~144µs) due to repeated regex searches and disk I/O; adding `@lru_cache` and pre-compiling the regex pattern brought it down to ~9µs (~15x speedup).
**Action:** Always pre-compile JSON validators and regex patterns at the class or module level for frequently called paths. Use caching for static template loading.
