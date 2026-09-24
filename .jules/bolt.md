## 2025-05-18 - JSON Schema Validator Pre-compilation

**Learning:** Invoking `jsonschema.validate(instance, schema)` on every call constructs a validator class and resolves schema metaschemas dynamically each time, creating a major performance bottleneck in loops or frequent calls (~1.60s per 1000 iterations). Instantiating `validator_for(schema)(schema)` once on object initialization and calling `validator.validate(instance)` reuses compiled rules and yields a ~57x execution speedup (~0.027s per 1000 iterations).

**Action:** When performing schema validation on data instances with static or long-lived schemas, pre-compile the validator class via `jsonschema.validators.validator_for` during object initialization rather than using `jsonschema.validate` repeatedly.
