# Bolt Journal

## 2025-02-23 - Pre-compile jsonschema Validator Instance
**Learning:** Re-invoking `jsonschema.validate(instance, schema)` on every call causes `jsonschema` to rebuild the validator class and resolve schema properties repeatedly, leading to unnecessary CPU overhead during output schema validation. Pre-compiling the validator class/instance once on initialization via `jsonschema.validators.validator_for(schema)(schema)` yields a ~13-14x speedup per validation call.
**Action:** Always pre-compile validator instances when schema validation occurs repeatedly against a fixed JSON schema.
