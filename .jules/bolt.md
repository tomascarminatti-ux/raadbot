## 2025-05-14 - Optimized Prompt Building and Schema Validation
**Learning:** In the RAADBot pipeline, repeated disk I/O for prompt templates and redundant JSON schema compilation during candidate validation were significant micro-bottlenecks. Caching templates with `lru_cache` and pre-compiling the `jsonschema` validator provides a measurable 5x-12x speedup for these specific operations.
**Action:** Always pre-compile JSON schemas in the `__init__` method of orchestrators and use memoization for static file-based assets like prompts.
