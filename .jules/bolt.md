## 2025-05-14 - Pre-compiled JSON Schema Validation
**Learning:** Re-compiling a JSON schema on every validation call using `jsonschema.validate` introduces significant overhead (up to ~2.5ms per call). Using `jsonschema.validators.validator_for` to pre-compile the validator in `__init__` reduces this to ~0.18ms, a ~14x speedup.
**Action:** Always pre-compile `jsonschema` validators when validating multiple instances against the same schema.

## 2025-05-14 - Module-level Schema Caching
**Learning:** Loading and parsing a JSON schema from disk on every object instantiation is wasteful. Using a module-level global cache for the schema dictionary eliminates redundant I/O.
**Action:** Use a global `_SCHEMA_CACHE` for static configuration files that are loaded frequently across different class instances.
