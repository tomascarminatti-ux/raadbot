## 2025-02-12 - [Precompiling JSON Schema Validators]
**Learning:** In a Python service processing sequential pipelines with repeated validation of JSON outputs against schemas, calling `jsonschema.validate` repeatedly compiles the schema on every call, creating a significant CPU bottleneck. Precompiling the schema using `jsonschema.validators.validator_for` during object initialization improves validation performance tremendously.
**Action:** Always precompile the schema validator and reuse the validator instance for schema checks.
