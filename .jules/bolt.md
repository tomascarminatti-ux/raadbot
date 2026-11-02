# Bolt's Journal - Critical Learnings Only

## 2026-03-30 - Pre-compile jsonschema Validator Instances in Stateful Pipelines
**Learning:** In Python services using `jsonschema`, calling `jsonschema.validate(instance, schema)` repeatedly introduces significant overhead because each call resolves the schema validator class via `validator_for(schema)`, instantiates a new validator object, and checks schema specifications. Pre-compiling the validator instance once via `validator_for(schema)(schema)` and invoking `validator.validate(instance)` yields an ~8-14x speedup per validation call without sacrificing error reporting or schema accuracy.
**Action:** Always pre-compile `jsonschema` validator instances on pipeline initialization or module singleton instances instead of calling `jsonschema.validate(instance, schema)` repeatedly in iterative/batch pipelines.
