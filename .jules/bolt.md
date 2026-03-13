# Bolt Performance Journal

## 2025-05-23 - JSonSchema Pre-compilation Efficiency
**Learning:** Using `jsonschema.validate` in a loop is an anti-pattern because it re-parses the schema and creates a new validator class for every call. Pre-compiling with `validator_for` provides a ~13x speedup in this codebase.
**Action:** Always pre-compile JSON validators for static schemas in execution loops.

## 2025-05-23 - Redundant Template Processing
**Learning:** Calling `build_prompt` inside a validation retry loop is redundant if the prompt variables don't change. Hoisting it outside saves unnecessary string manipulation and disk I/O (if not cached).
**Action:** Hoist deterministic prompt construction outside of retry loops.
