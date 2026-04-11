## 2025-05-22 - [JSON Schema Validation Optimization]
**Learning:** `jsonschema.validate()` is a significant bottleneck when called repeatedly because it re-parses the schema and re-initializes the validator class on every call. In this codebase, it was taking ~2.5ms per call, which was much slower than prompt construction (~0.1ms).
**Action:** Pre-compile the validator using `jsonschema.validators.validator_for(schema)(schema)` during class initialization. This reduced validation latency by ~93% to ~0.19ms per call.
