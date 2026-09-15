## 2026-03-31 - Pre-compile JSON Schema Validators in Pipeline
**Learning:** Standard `jsonschema.validate(instance, schema)` creates a new validator instance and parses/resolves JSON schema definitions on every single call. Pre-compiling the validator using `jsonschema.validators.validator_for(schema)(schema)` once on pipeline initialization speeds up validation by ~13.4x (from 5.46s down to 0.41s for 2,000 iterations).
**Action:** Always pre-compile JSON schema validators when validating structured model outputs repeatedly within pipeline loops.
