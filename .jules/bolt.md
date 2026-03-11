## 2025-05-14 - [JSON Schema Validation Overhead]
**Learning:** Using `jsonschema.validate` repeatedly is expensive (~2.5ms per call) because it re-parses the schema and discovers the validator class every time.
**Action:** Pre-compile the validator using `jsonschema.validators.validator_for(schema)(schema)` and store it on the class/module level. This reduces latency to ~16μs per call (~154x speedup).
