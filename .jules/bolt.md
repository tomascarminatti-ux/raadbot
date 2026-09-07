## 2026-03-01 - Pre-compiling JSON Schema Validators
**Learning:** Calling `jsonschema.validate(instance, schema)` repeatedly on every GEM output validation recreates and resolves the JSON Schema validator class on every call. Pre-compiling the validator using `jsonschema.validators.validator_for(schema)(schema)` once during `Pipeline.__init__` yields a ~13.5x speedup (from 5.27s down to 0.39s over 2,000 validations).
**Action:** Always pre-compile JSON schema validators in class initializers when schema structure is static across pipeline runs.
