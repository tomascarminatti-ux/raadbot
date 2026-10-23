# Bolt's Performance Journal

## 2026-03-30 - Pre-compile JSON Schema Validators for Repeated Validation
**Learning:** Calling `jsonschema.validate(instance, schema)` repeatedly re-creates and resolves the validator instance on every validation call, adding significant overhead (~2.6ms per call). Pre-compiling the validator using `jsonschema.validators.validator_for(schema)(schema)` during initialization reduces validation overhead to ~0.2ms per call (~13x speedup).
**Action:** Always pre-compile JSON Schema validator instances in class `__init__` when validating JSON payloads in hot paths.
