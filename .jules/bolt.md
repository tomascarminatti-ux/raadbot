# Bolt's Performance Journal

## 2026-02-21 - Pre-compiling jsonschema validators in Python
**Learning:** Calling `jsonschema.validate(instance=..., schema=...)` dynamically determines the appropriate validator class and parses/validates the schema dictionary on every single call. Pre-compiling the validator once via `validator_for(schema)(schema)` and reusing `validator.validate(instance)` avoids repeated schema introspection, resulting in a ~12-13x speedup per validation call.
**Action:** When validating data repeatedly against a static JSON schema, instantiate and reuse a validator instance via `validator_for(schema)(schema)` instead of invoking `validate()`.
