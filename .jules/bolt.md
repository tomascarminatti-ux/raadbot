## 2026-03-30 - Pre-compiling jsonschema Validators

**Learning:** Calling `jsonschema.validate(instance, schema)` repeatedly re-parses and re-instantiates schema validator classes on every validation call, adding ~3.6 ms of overhead per call. By instantiating `jsonschema.validators.validator_for(schema)(schema)` once on object initialization (`Pipeline.__init__`) and calling `validator.validate(instance)`, schema validation time drops from ~3.64 ms/call to ~0.19 ms/call (~19x speedup).

**Action:** Always pre-compile JSON schema validators when validating repeated data instances in stateful classes or pipelines instead of calling top-level `jsonschema.validate()`.
