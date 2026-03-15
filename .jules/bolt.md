## 2025-05-15 - [Prompt Template Caching]
**Learning:** Frequent disk I/O in `prompt_builder.py` during orchestration (especially with multiple candidates and recursive GEM calls) significantly impacts latency. Using `lru_cache` to memoize template loading provides a measurable speedup without breaking the system.
**Action:** Always consider caching static assets like prompt templates in agentic systems to reduce per-step overhead.
