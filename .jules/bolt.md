# Bolt's Performance Journal ⚡

## 2025-05-15 - [Initial Discovery: JSON Schema Validation Bottleneck]
**Learning:** The `jsonschema.validate` function re-parses and re-compiles the schema on every call. In a pipeline with multiple steps and many candidates, this adds significant overhead. Pre-compiling the validator using `jsonschema.Draft7Validator` (or similar) can provide a ~60x speedup for the validation step.
**Action:** Use pre-compiled validators when performing repeated schema validations against the same schema.
