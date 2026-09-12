## 2025-05-15 - Pre-compiling jsonschema Validators for High-Throughput Pipelines

**Learning:** Invoking `jsonschema.validate(instance, schema)` repeatedly in hot loops causes high performance overhead because `jsonschema` re-initializes schema validators and type checkers for every call. Pre-compiling the validator using `jsonschema.validators.validator_for(schema)(schema)` once during initialization and reusing the validator instance yields a ~13.8x validation speedup (e.g., from 4.65s down to 0.33s per 2,000 iterations).

**Action:** Whenever JSON schema validation is performed repeatedly on incoming API requests or pipeline outputs with a fixed schema, instantiate and store the validator object (`self.validator = validator_for(schema)(schema)`) at initialization time instead of calling `jsonschema.validate()`.
