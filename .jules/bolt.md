## 2025-02-22 - Pre-compiling jsonschema Validators

**Learning:** `jsonschema.validate(instance, schema)` dynamically reconstructs and compiles schema validator rules on every call. Pre-instantiating the schema validator instance once using `jsonschema.validators.validator_for(schema)(schema)` during class initialization yields a ~13x performance improvement per validation call.
**Action:** Always pre-instantiate `validator_for(schema)(schema)` when performing repeated schema validation against a fixed schema in pipeline or client loops.
