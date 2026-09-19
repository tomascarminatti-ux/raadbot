# Bolt's Journal - Critical Performance Learnings

## 2025-02-15 - JSON Schema Pre-compilation
**Learning:** Pre-compiling `jsonschema` validators using `jsonschema.validators.validator_for` during initialization yields a 12-14x speedup compared to calling `jsonschema.validate()` repeatedly.
**Action:** Always precompile schema validators when validating multiple instances against static schemas.

## 2025-02-16 - File mtime LRU Caching
**Learning:** Caching disk I/O and file parsing using `@functools.lru_cache` keyed on `(filepath, mtime)` provides a ~5-8x speedup while guaranteeing invalidation when files change.
**Action:** Use mtime-based LRU caching for static/semi-static asset loading like contracts, input files, and prompt templates.
