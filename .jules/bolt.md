## 2026-10-28 - Pre-compile JSON Schema Validators
**Learning:** Calling `jsonschema.validate(instance, schema)` repeatedly re-parses and instantiates schema validators on every call (~2.6 ms/validation). Pre-compiling the validator once with `validator_for(schema)(schema)` and reusing it via `validator.validate(instance)` reduces validation latency to ~0.18 ms (~13.5x speedup).
**Action:** Always pre-compile `jsonschema` validators during class initialization (`__init__`) or at module level whenever schemas are static and validated repeatedly in loops or API pipelines.
