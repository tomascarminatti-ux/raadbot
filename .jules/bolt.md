## 2026-03-31 - Pre-compiling jsonschema validators in long-running/pipeline contexts

**Learning:** Calling `jsonschema.validate(instance, schema)` repeatedly triggers `validator_for(schema)(schema)` creation overhead on every call (~2.6ms per validation). Pre-compiling `validator_cls(schema)` once during class initialization and reusing `validator.validate(instance)` reduces validation latency to ~0.19ms per call (~12-13.5x speedup).

**Action:** In classes or loops performing schema validations repeatedly, always instantiate and store the compiled `validator` instance during initialization rather than calling `jsonschema.validate()` per invocation.
