# Bolt's Journal - Critical Learnings

## 2026-03-29 - Pre-compiling JSON Schema Validators in Pipeline
**Learning:** Calling `jsonschema.validate(instance, schema)` repeatedly causes `jsonschema` to resolve and re-compile the JSON schema on every single function call. Pre-compiling the validator using `jsonschema.validators.validator_for(schema)(schema)` once during class initialization (`Pipeline.__init__`) and reusing `validator.validate(instance)` yields a ~13.1x speedup per validation call (reducing runtime from ~5.17s to ~0.39s over 2,000 validation runs).
**Action:** When validating data structures against a static or recurring JSON Schema, always pre-compile the validator instance during class initialization instead of invoking `jsonschema.validate` directly.
