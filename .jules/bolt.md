## 2025-05-22 - Optimized JSON Validation and Prompt Caching

**Learning:** Pre-compiling JSON schemas with `jsonschema.validators.validator_for` provides a massive speedup (~13.5x) over calling `validate()` directly, especially in long-running pipelines where the same schema is reused. Additionally, disk I/O for prompt templates can be eliminated using `functools.lru_cache`, which is safe for static template files.

**Action:** Always pre-compile JSON validators at the class or module level when the schema is static. Use `lru_cache` for file-based template loaders to reduce latency in parallel processing loops.
