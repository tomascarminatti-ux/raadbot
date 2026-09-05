## 2026-03-30 - Pre-compiling JSON Schema Validator in Pipeline

**Learning:** `jsonschema.validate` recompiles and validates schema metadata on every single call. Pre-compiling the schema using `jsonschema.validators.validator_for(schema)(schema)` once during class initialization (`Pipeline.__init__`) and calling `validator.validate(json_data)` eliminates schema parsing/compilation overhead on repeated GEM step output validations.
**Action:** Always pre-compile JSON schema validator instances when performing repeated schema validations against a fixed schema.
