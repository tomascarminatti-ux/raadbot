# Bolt's Journal - Critical Learnings

## 2026-09-18 - Pre-compiled JSON Schema Validator in Pipeline
**Learning:** Calling `jsonschema.validate(instance, schema)` repeatedly parses and builds validator classes on every invocation. In `Pipeline`, where output JSONs from GEM steps are validated against the output schema on every GEM execution (and on validation retry loops), pre-compiling the schema using `jsonschema.validators.validator_for(schema)(schema)` once during class initialization speeds up validation by ~12x.
**Action:** Always pre-compile `jsonschema` validators when validating multiple instances against the same schema in hot paths or long-running pipelines.
