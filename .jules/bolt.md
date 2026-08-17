## 2026-03-30 - Pre-compiling jsonschema validator

**Learning:** Invoking `jsonschema.validate(instance, schema)` dynamically parses and constructs validator rules on every call, leading to significant CPU overhead when validating multiple LLM outputs against a JSON schema. Pre-compiling the schema once via `jsonschema.validators.validator_for(schema)(schema)` during object initialization yields a ~13x execution speedup (~0.4s vs ~5.4s for 2,000 iterations).

**Action:** Whenever JSON schemas are validated repeatedly in loop or pipeline workflows, instantiate the pre-compiled validator in `__init__` or a module-level constant and reuse `validator.validate(instance)` directly.
