# Bolt's Journal - Critical Performance Learnings

## 2026-02-21 - Pre-compile jsonschema validators for high-throughput pipeline validation
**Learning:** `jsonschema.validate(instance, schema)` dynamically calls `validator_for(schema)(schema)` to construct a validator class and compile rules on every invocation. In workloads with repeated validations against a static schema (e.g. GEM outputs across multiple candidates and retries), this adds ~2.6-3.0 ms per validation call. Pre-compiling the validator instance once (`validator_for(schema)(schema)`) and calling `validator.validate(instance)` takes ~0.19 ms per call—delivering a ~13-14x speedup per validation call.
**Action:** When performing schema validation on repeated payloads or inside loops/pipelines, never call `jsonschema.validate(instance, schema)` repeatedly. Pre-compile the validator instance once on class or module initialization using `jsonschema.validators.validator_for(schema)(schema)`.
