## 2025-05-15 - Optimized Prompt Building Performance

**Learning:** Repeated disk I/O for prompt templates and multiple `.replace()` calls for variable injection created a measurable bottleneck (approx. 0.14ms per build). Using `lru_cache` for template loading and a single-pass `re.sub` with a callback reduced latency by ~70%.

**Action:** Always use `functools.lru_cache` for static file loading and prefer single-pass regex substitution over chained `.replace()` calls when injecting multiple variables into a template.
