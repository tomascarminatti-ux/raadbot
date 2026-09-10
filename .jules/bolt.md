## 2026-09-10 - Pre-compiling jsonschema validator for recurrent pipeline validations

**Learning:** `jsonschema.validate` dynamically resolves and builds a validator class on every invocation, causing significant overhead (~2.5ms per call) when validating structured LLM outputs in pipeline loops. Pre-compiling the validator instance once via `jsonschema.validators.validator_for(schema)(schema)` and invoking `validator.validate(data)` reduces schema validation overhead from ~2.5ms to ~0.19ms per call (~13.3x speedup).
**Action:** Always pre-compile JSON Schema validators during class initialization when schema validation runs repeatedly in hot paths or worker loops.
