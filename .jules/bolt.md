# Bolt's Performance Journal

## 2025-05-20 - JSON Schema Validation Bottleneck
**Learning:** The `jsonschema.validate` function in Python is slow for repeated calls because it re-parses the schema and re-instantiates the validator every time. Pre-compiling the validator using `validators.validator_for` and reusing it provides a massive performance boost.
**Action:** Always pre-compile JSON Schema validators in `__init__` if validation is performed repeatedly within the same object lifecycle.
