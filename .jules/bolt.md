# Bolt's Journal - Critical Learnings

## 2025-01-24 - Pre-compile JSON Schema Validator
**Learning:** Instantiating `jsonschema.validate` repeatedly in performance-sensitive pipelines compiles the schema on every single invocation, leading to significant overhead. Pre-compiling the validator using `validator_for(schema)` and storing the validator instance (e.g., `self.validator`) can result in a ~14x validation speedup.
**Action:** Always precompile JSON schemas into a single reusable validator instance when they need to be validated repeatedly.
