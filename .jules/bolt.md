# Bolt's Journal - Critical Performance Learnings

## 2026-09-16 - Pre-compiling JSON Schema Validators
**Learning:** Calling `jsonschema.validate(instance, schema)` repeatedly re-creates and compiles the validator class on every function call, introducing substantial validation overhead (~2.5ms per call). Pre-instantiating the validator class with `validator_for(schema)(schema)` once on object initialization and reusing `.validate(instance)` reduces validation time down to ~0.17ms per call (a ~14.6x execution speedup).
**Action:** When validating standard JSON output schemas across multiple API pipeline requests or iterations, pre-compile the validator instance during class initialization instead of invoking top-level `validate()`.
