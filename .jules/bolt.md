# Bolt's Performance Journal

## 2026-03-30 - Pre-compiled JSONSchema Validator Optimization
**Learning:** Calling `jsonschema.validate(instance, schema)` dynamically resolves and reconstructs the validator class and rules on every call. In pipelines validating repeated structured outputs against a static contract schema (like `gem_output.schema.json`), pre-compiling the validator via `validator_for(schema)(schema)` and invoking `validator.validate(instance)` yields a ~13-17x speedup (reducing per-call validation time from ~3.2ms to ~0.19ms).
**Action:** When performing schema validation on repeated inputs/outputs in pipeline execution loops, instantiate and reuse the validator instance on the orchestrator class rather than repeatedly calling `jsonschema.validate()`.
