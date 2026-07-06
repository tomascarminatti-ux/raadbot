## 2025-05-14 - Optimized Prompt Construction and Contract Validation
**Learning:** Eliminating redundant disk I/O and iterative string replacements in prompt construction and schema validation provides order-of-magnitude speedups in LLM-intensive pipelines. Using `lru_cache` for templates and schemas, combined with a single-pass `re.sub` for variable injection, reduced prompt building time from ~0.08ms to ~0.002ms (~40x speedup).
**Action:** Always prefer caching for static or semi-static file reads (templates, schemas) and use single-pass string manipulation for complex template injections.

## 2025-05-14 - Safe Benchmarking Practices
**Learning:** Benchmarking scripts should never modify or overwrite production data files (e.g., schemas in `contracts/`). This can lead to regressions and corrupted application state.
**Action:** Use `tempfile` for creating transient test data during benchmarks and ensure original file state is preserved.
