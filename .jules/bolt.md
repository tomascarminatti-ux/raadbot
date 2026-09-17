## 2026-03-31 - Pre-compiling jsonschema validator instances
**Learning:** Calling `jsonschema.validate(instance, schema)` repeatedly parses and constructs a validator class every single invocation, incurring substantial overhead (e.g. 4.94s vs 0.35s for 2,000 validations, ~14x speedup).
**Action:** Pre-compile schema validators once during initialization using `jsonschema.validators.validator_for(schema)(schema)` and reuse the validator instance (`self.validator.validate(data)`).
