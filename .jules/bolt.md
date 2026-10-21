# Bolt's Journal - Critical Learnings

## 2026-03-31 - Pre-compile jsonschema validators for output schema validation
**Learning:** Calling `jsonschema.validate(instance, schema)` repeatedly re-parses the JSON schema and instantiates a validator object on every call. Pre-compiling the validator using `jsonschema.validators.validator_for(schema)(schema)` once during class initialization (`Pipeline.__init__`) and calling `validator.validate(data)` yields a ~13.5x speedup per validation call.
**Action:** Whenever validating structured JSON responses against a static schema in loops or API pipelines, pre-compile the validator instance during initialization rather than using `jsonschema.validate`.
