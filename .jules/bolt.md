## 2025-05-15 - [JSON Schema Optimization with Pre-compilation and Caching]
**Learning:** In `jsonschema` (v4.21.1+), using `jsonschema.validate()` repeatedly is expensive as it re-resolves and re-compiles the schema every time (~3.9ms in this env). Pre-compiling the validator in the constructor and caching the schema at the module level reduces latency by >90% (~0.3ms). Also, `validator_for` should be imported from `jsonschema.validators` to avoid deprecation warnings.
**Action:** Always pre-compile `jsonschema` validators if they are used in hot paths or loops.
