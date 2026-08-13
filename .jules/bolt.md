# Bolt's Performance Journal

This journal documents critical, codebase-specific performance learnings to avoid regressions and guide future optimizations.

## 2026-03-02 - JSON Schema Pre-compilation
**Learning:** Compiling JSON Schema using `jsonschema.validators.validator_for` upfront and reusing the validator instance on the same schema avoids the costly process of schema parsing, resolution, and validator-class lookup for every single validation, leading to a ~12.6x performance speedup in schema validation.
**Action:** Always pre-compile JSON schemas when they are used repeatedly, rather than calling the raw `jsonschema.validate` function in hot paths.
