## 2025-05-15 - Prompt Construction Optimization
**Learning:** Using `re.sub` with a callback for variable substitution in prompt templates is significantly more efficient than nested loops of `str.replace()`, especially as the number of variables or the template size increases. Combined with `lru_cache` for template loading, latency dropped from ~0.13ms to ~0.013ms per call.
**Action:** Always prefer single-pass regex substitution for templating systems. Ensure cache invalidation is implemented if templates can be updated at runtime.
