# Bolt's Journal - Critical Learnings Only

## 2025-02-15 - Compile JSON Schema Validator Once
**Learning:** Repeatedly calling `jsonschema.validate` parses the schema and creates a new validator class internally every single time, which is extremely expensive (~15x overhead). Pre-compiling the validator class using `jsonschema.validators.validator_for` during object initialization and reusing the compiled validator instance eliminates this overhead.
**Action:** Always pre-compile JSON schemas and reuse the validator instance for any high-frequency validation steps in Python.
