## 2026-03-01 - Pre-compiling jsonschema validator instance

**Learning:** `jsonschema.validate(instance, schema)` dynamically looks up and creates validator classes on every invocation, adding unnecessary parsing and object creation overhead when validating multiple documents against a fixed schema. Pre-instantiating the validator via `validator_for(schema)(schema)` during class initialization avoids repeated schema parsing and yields a ~13.8x - 14.2x speedup during output validations.

**Action:** Whenever a fixed JSON Schema is evaluated repeatedly (such as pipeline output validation or API contract checks), pre-compile and retain the validator instance on initialization rather than calling helper functions like `jsonschema.validate`.
