# Bolt Journal - Critical Learnings

## 2026-03-30 - Precompiling JSON Schema Validators
**Learning:** Calling `jsonschema.validate(instance, schema)` repeatedly inside hot execution loops (such as validating LLM outputs across multiple GEM steps/candidates) incurs significant performance overhead because `jsonschema.validate` resolves schema meta-schemas and instantiates validator classes on every invocation. Precompiling the validator class during `Pipeline` initialization using `jsonschema.validators.validator_for(schema)(schema)` and reusing `self.validator.validate(instance)` yields a ~14x speedup (0.35s vs 5.08s for 2,000 validations) without changing behavior or sacrificing error reporting.
**Action:** Always precompile schema validators during object initialization when validating multiple JSON payloads against a fixed JSON schema.
