# Bolt's Performance Journal

## 2026-02-21 - Pre-compiling jsonschema Validators
**Learning:** In Python's `jsonschema` library, calling `validate(instance, schema)` dynamically resolves the validator class (via `validator_for`), builds a resolver, and checks the schema specification on every invocation. For a fixed schema used across multiple validation cycles (such as GEM output schema validation across multiple candidates and GEM steps), pre-instantiating the validator class once via `validator_for(schema)(schema)` and invoking `validator.validate(instance)` eliminates this overhead, yielding a ~13-14x speedup per validation call (~0.20ms vs ~2.60ms).
**Action:** When performing schema validation on repeated inputs in pipeline or request processing loops, compile the validator once during class initialization (`__init__`) or at module level rather than calling `jsonschema.validate(instance, schema)` repeatedly.
