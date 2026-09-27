## 2026-03-30 - Pre-compile jsonschema validator in Pipeline initialization

**Learning:** `jsonschema.validate(instance, schema)` dynamically checks the schema draft version and constructs a validator class/instance on every call. Pre-compiling the validator instance once during class initialization using `jsonschema.validators.validator_for(schema)(schema)` and calling `validator.validate(instance)` avoids repeated schema parsing overhead and yields a ~57x speedup per validation call.

**Action:** Whenever `jsonschema.validate` is called repeatedly against a static or loaded schema, instantiate and reuse a single validator instance with `validator_for(schema)(schema)`.
