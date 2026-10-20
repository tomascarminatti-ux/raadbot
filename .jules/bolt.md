# Bolt's Journal - Critical Performance Learnings

## 2026-10-20 - Pre-compiling jsonschema validator for repeated schema validation
**Learning:** `jsonschema.validate(instance, schema)` dynamically resolves and compiles the validator class on every function call. For workflows where every model response is validated against a static output schema (`gem_output.schema.json`), pre-compiling the validator once via `jsonschema.validators.validator_for(schema)(schema)` and reusing `validator.validate(instance)` eliminates schema resolution overhead, yielding a ~13.5x speedup per validation call.
**Action:** Always pre-compile JSON schemas when validating multiple payloads against a fixed schema in pipeline or API handlers.
