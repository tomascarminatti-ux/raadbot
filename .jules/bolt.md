## 2025-05-14 - [JSON Schema Validator Pre-compilation]
**Learning:** In Python's `jsonschema` library, using the high-level `validate()` function incurs significant overhead (~2.7ms per call) because it re-parses the schema and re-identifies the validator class every time. Pre-compiling the validator in the constructor using `validators.validator_for(schema)(schema)` reduced validation latency to ~0.19ms (~93% improvement).
**Action:** Always pre-compile JSON validators when the schema is static and validation is performed multiple times in a hot path.
