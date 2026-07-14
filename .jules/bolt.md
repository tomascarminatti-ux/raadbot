## 2025-05-15 - Optimized Prompt Construction
**Learning:** Repetitive disk I/O and multiple string replacements in the prompt builder were causing a bottleneck (~0.11ms per call). Using `lru_cache` for template loading and a single-pass `re.sub` with a callback improved performance by ~26x.
**Action:** Always prefer single-pass regex replacement for multi-variable templates and use caching for static or semi-static assets like prompt files. Ensure cache invalidation is handled when source data changes (e.g., via the refinement endpoint).
