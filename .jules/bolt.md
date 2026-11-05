# Bolt's Performance Journal

## 2025-05-18 - Pre-compile JSONSchema Validators
**Learning:** `jsonschema.validate(instance, schema)` dynamically calls `validator_for(schema)`, validates the schema itself, and constructs a new validator class instance on every single call. In pipelines with frequent validation steps (like GEM evaluations and retries), this causes unnecessary CPU overhead (~2.66ms per call vs ~0.21ms when pre-compiled, ~12.5x speedup).
**Action:** When validating recurring JSON payloads against a static schema, construct and cache the validator instance during class initialization (`self.validator = validator_for(schema)(schema)`) and reuse `self.validator.validate(instance)`.
