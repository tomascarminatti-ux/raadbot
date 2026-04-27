## 2026-04-27 - Optimized Prompt Construction Latency
**Learning:** Prompt construction was incurring redundant disk I/O and regex compilation overhead in each GEM step. Implementing `lru_cache` for template loading and pre-compiling the variable substitution regex reduced latency significantly.
**Action:** Always implement caching for static assets like prompt templates and pre-compile frequently used regex patterns in hot paths.
