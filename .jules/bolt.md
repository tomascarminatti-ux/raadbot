# Bolt's Journal - Critical Learnings Only

## 2026-03-05 - JSON Schema Validator Compilation Overhead
**Learning:** Standard `jsonschema.validate` resolves schema types, retrieves metadata, and builds validator instances dynamically on every single call. In high-throughput async processing or batch iteration, this compile-on-the-fly behavior introduces significant CPU bottlenecks.
**Action:** Always pre-compile JSON Schema validators once at initialization and reuse them across multiple validation calls, using `jsonschema.validators.validator_for` or the specific validator class (e.g. `Draft7Validator`).

### Performance Benchmark Results:
- **Baseline (Standard `jsonschema.validate`):** 5.25 seconds for 2,000 iterations
- **Optimized (Pre-compiled validator):** 0.38 seconds for 2,000 iterations
- **Speedup:** ~13.74x faster!
