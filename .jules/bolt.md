# Bolt's Performance Optimization Journal

## 2026-03-05 - JSON Schema Validator Pre-compilation
**Learning:** Calling `jsonschema.validate` repeatedly compiles the schema dynamically on every execution, causing significant CPU overhead (up to ~15x slower on standard GEM schemas). Pre-compiling the schema using `jsonschema.validators.validator_for` during object initialization yields massive speedups by avoiding redundant schema parsing and compilation overhead.
**Action:** Always pre-compile JSON schemas during instance initialization when validation is expected to run multiple times (e.g., inside loops or pipelines).
