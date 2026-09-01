## 2026-03-31 - Pre-compiling jsonschema validator in Pipeline
**Learning:** `jsonschema.validate(instance, schema)` dynamically resolves and compiles the validator class and schema on every single invocation. In pipelines or loops where the schema is fixed, pre-compiling the validator once with `jsonschema.validators.validator_for(schema)(schema)` yields a ~60x speedup per validation call.
**Action:** Always pre-compile `jsonschema` validators during class initialization (`__init__`) or module load when validating against static schemas.
