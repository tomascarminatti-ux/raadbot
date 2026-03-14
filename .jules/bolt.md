## 2025-03-14 - JSON Schema Validation Bottleneck
**Learning:** `jsonschema.validate` is surprisingly expensive (~2.8ms per call) compared to other orchestration tasks like prompt building (~0.1ms). This is because it re-resolves the validator and re-validates the schema itself on every call.
**Action:** Always use pre-compiled validators via `jsonschema.validators.validator_for(schema)` when performing repeated validations against the same schema.
