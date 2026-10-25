# Bolt's Performance Journal

## 2026-03-31 - Pre-compiling jsonschema validators in Pipeline
**Learning:** In `agent/pipeline.py`, calling `jsonschema.validate(instance, schema)` repeatedly on every GEM output validation recreates and resolves validator instances from scratch each time. By obtaining the schema validator class using `jsonschema.validators.validator_for(schema)` and pre-instantiating `self.validator = validator_cls(self.schema)` during `Pipeline.__init__`, subsequent validation calls (`self.validator.validate(json_data)`) run ~13.5x faster (from ~2.65s down to ~0.20s per 1000 calls).
**Action:** Always pre-compile or pre-instantiate `jsonschema` validator instances when validating JSON structures against static or reusable schemas in long-lived pipeline/service instances.
