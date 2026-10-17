## 2026-03-31 - Pre-compiling jsonschema validator yields ~15x validation speedup

**Learning:** `jsonschema.validate(instance, schema)` dynamically resolves and compiles the schema validator class (`validator_for(schema)(schema)`) on every single invocation. In pipelines or loop iterations where the JSON schema remains static, re-compiling the validator class introduces redundant overhead (~2.6s vs ~0.17s per 1000 validations).

**Action:** When validating data repeatedly against a static JSON schema, instantiate and reuse the validator instance once (`validator = validator_for(schema)(schema)`) during class or component initialization and invoke `validator.validate(data)`.
