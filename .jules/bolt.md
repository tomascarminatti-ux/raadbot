## 2026-09-14 - Pre-compile jsonschema validators in Pipeline

**Learning:** `jsonschema.validate(instance, schema)` dynamically resolves and compiles the JSON schema validator on every single invocation, introducing significant execution overhead. In long-running or batch pipeline operations, pre-compiling the validator using `jsonschema.validators.validator_for(schema)(schema)` once upon initialization and reusing `validator.validate(instance)` eliminates repetitive schema parsing overhead, resulting in a ~60x performance speedup (e.g. 5.15s reduced to 0.08s across 2,000 iterations).

**Action:** Whenever validating structured data against a fixed schema repeatedly (such as JSON output validation in agent pipelines), pre-compile the validator instance during class initialization (`__init__`) and store `self.validator`.
