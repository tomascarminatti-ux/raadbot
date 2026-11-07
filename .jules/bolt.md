# Bolt's Journal - Critical Learnings

## 2026-03-30 - Pre-compiling jsonschema Validator
**Learning:** Calling `jsonschema.validate(instance, schema)` on each validation invocation parses and compiles the schema validator from scratch every time (~2.7ms per call for `gem_output.schema.json`). By compiling the validator instance once (`validators.validator_for(schema)(schema)`) during pipeline initialization and calling `validator.validate(instance)`, validation latency drops to ~0.2ms per call (~12.5x-13x speedup) without changing schema definitions or external APIs.
**Action:** Always pre-compile `jsonschema` validators on classes or module singletons when the schema is static and validations occur frequently or in batch pipelines.
