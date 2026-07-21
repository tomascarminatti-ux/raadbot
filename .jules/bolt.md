# Bolt's Performance Journal

This journal tracks critical codebase-specific performance learnings, bottlenecks, and anti-patterns discovered during development.

## 2026-03-01 - JSON Schema Compilation Overhead in Sequential Pipeline Runs
**Learning:** In high-frequency or parallel executions (such as running candidate assessments concurrently), invoking `jsonschema.validate` directly incurs substantial CPU overhead because the schema is parsed, resolved, and compiled into a validator class from scratch on every single invocation. Pre-compiling the validator using `jsonschema.validators.validator_for` during pipeline initialization avoids this redundant work, improving schema validation performance by ~14x (reducing CPU time for 2,000 runs from ~4.93s to ~0.36s).
**Action:** Always pre-compile JSON Schemas or validators if they are evaluated multiple times during the lifespan of an application or session, especially inside loops or concurrent async processes where CPU-bound overhead blocks the Python event loop.
