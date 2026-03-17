# Bolt's Performance Journal

This journal records critical performance learnings for the Raadbot project.

## 2025-05-15 - JSON Schema Pre-compilation
**Learning:** Using `jsonschema.validate()` in a loop or repeated execution (like the GEM pipeline) is highly inefficient as it re-validates the schema itself and creates a new validator instance on every call. Pre-compiling the validator with `jsonschema.validators.validator_for(schema)(schema)` and reusing it provides a ~60x speedup for the validation step.
**Action:** Always pre-compile JSON schemas in the constructor or module level when validation is performed repeatedly.
