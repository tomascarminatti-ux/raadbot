# Bolt's Journal - Critical Performance Learnings

## 2026-03-30 - Pre-compiling JSON Schema Validator for Repeated Pipeline Validation
**Learning:** Calling `jsonschema.validate(instance, schema)` repeatedly constructs and initializes a validator class and schema mapping from scratch on every call. Pre-compiling the validator class and instance using `jsonschema.validators.validator_for(schema)(schema)` during initialization yields a ~14x speedup for JSON schema validation of agent outputs in `Pipeline`.
**Action:** When validating JSON objects against a fixed schema repeatedly (e.g. LLM structured outputs in pipeline execution), pre-instantiate the validator in `__init__` and reuse `validator.validate(data)`.
