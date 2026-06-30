# Bolt's Journal - Critical Performance Learnings

## 2025-05-14 - Optimized Prompt Construction
**Learning:** In Python, repeated `str.replace` calls create many intermediate string objects. For a template with many variables, a single-pass `re.sub` with a callback is significantly faster. Combining this with `lru_cache` for I/O results in a ~35x speedup for prompt construction.
**Action:** Use `lru_cache` for template I/O and `re.sub` for batch variable replacement in performance-critical text processing.

## 2025-05-14 - Schema Validation Overhead
**Learning:** Loading and parsing JSON schemas for every validation call is a redundant bottleneck.
**Action:** Extract schema loading to a helper function decorated with `lru_cache` to ensure each unique schema is read and parsed from disk only once.
