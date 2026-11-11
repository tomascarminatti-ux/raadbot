# Bolt's Journal - Critical Learnings Only

## 2026-03-30 - jsonschema Pre-Compilation Speedup
**Learning:** Calling `jsonschema.validate(instance, schema)` repeatedly re-resolves the validator class and re-checks schema meta-specifications on every invocation. In batch pipeline runs evaluating multiple GEMs per candidate, this incurred significant CPU overhead. Using `validator_for(schema)(schema)` once on pipeline initialization yields a ~14x speedup per validation call.
**Action:** Always pre-compile JSON schemas with `validator_for(schema)(schema)` and reuse the validator instance across loop/batch iterations rather than invoking the module-level `validate()`.
