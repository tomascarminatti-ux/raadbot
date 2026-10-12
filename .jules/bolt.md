## 2026-03-31 - Pre-compile JSON Schema Validators in Async Pipelines

**Learning:** Invoking `jsonschema.validate(instance, schema)` on every API response validation re-evaluates and builds the schema validator instance each time, causing notable CPU overhead (~2.6ms per call). Pre-compiling the validator using `jsonschema.validators.validator_for(schema)(schema)` once in `__init__` reduces validation latency to ~0.18ms (~14x speedup per call).
**Action:** Always pre-compile `jsonschema` validators on class initialization or module load when validating repetitive JSON structures in pipelines or API handlers.
