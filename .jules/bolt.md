## 2025-05-22 - Pre-compiled JSON Schema Validator
**Learning:** Using `jsonschema.validate` repeatedly for the same schema is inefficient because it parses and compiles the schema on every call. Pre-compiling with `jsonschema.Draft7Validator` (or the appropriate validator class) provides a significant performance boost (~14x in this environment).
**Action:** Always pre-compile JSON schemas when they are used multiple times within the same object lifecycle.
