# Bolt's Journal - Performance Learnings

## 2026-02-13 - Pre-compiled JSON Schema Validators
**Learning:** Re-invoking `jsonschema.validate(data, schema)` repeatedly causes `jsonschema` to re-create and resolve the validator class each time, adding significant runtime overhead (~15x per call). Using `jsonschema.validators.validator_for(schema)(schema)` to construct a reusable validator instance on initialization eliminates this overhead completely.
**Action:** Always pre-compile JSON schemas into a validator instance during class initialization (`__init__`) or at module level if the schema is static.
