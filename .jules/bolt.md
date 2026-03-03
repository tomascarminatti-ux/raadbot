## 2024-03-03 - Compiled JSON Schema Validator
**Learning:** Pre-compiling a JSON Schema validator using `jsonschema.validators.validator_for` instead of calling `jsonschema.validate` repeatedly provides a ~13.6x speedup (from 2.6ms to 0.19ms per validation).
**Action:** Always pre-compile schemas when they are used multiple times (e.g., in loops or across different stages of a pipeline).

## 2024-03-03 - LRU Caching for Disk I/O
**Learning:** Adding `@lru_cache` to functions that read static templates from disk (like prompts) significantly reduces latency. Prompt building was sped up by ~3.67x (from 113μs to 31μs) by caching template reads.
**Action:** Use `functools.lru_cache` for expensive disk I/O on assets that do not change during the application's runtime.
