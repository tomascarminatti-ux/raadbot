# Bolt's Journal - Critical Learnings

## 2026-03-31 - Precompiling JSON Schema Validators
**Learning:** Calling `jsonschema.validate(instance, schema)` repeatedly re-creates and compiles the schema validator class from scratch on every invocation. Pre-compiling the validator class and instance using `jsonschema.validators.validator_for(schema)(schema)` and invoking `validator.validate(instance)` yields a ~12-14x speedup (e.g. 5.36s vs 0.42s per 2,000 validations) in JSON schema validation.
**Action:** Always pre-compile `jsonschema` validators during class initialization or module loading when validating multiple JSON payloads against a fixed schema.
