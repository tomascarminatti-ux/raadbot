# Bolt's Journal

## 2026-03-05 - JSON Schema Pre-compilation
**Learning:** In Python's `jsonschema` library, calling `jsonschema.validate(instance, schema)` repeatedly on every validation step recreates and compiles the schema validator from scratch, causing significant performance degradation. Precompiling the validator using `jsonschema.validators.validator_for` once during initialization and reusing it on each validation call yields an outstanding ~13.5x speedup.
**Action:** Always pre-compile JSON Schema validators when validating multiple instances/outputs in loop-based pipelines or server endpoints.
