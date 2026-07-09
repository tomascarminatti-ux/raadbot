## 2025-05-15 - Optimization of Prompt Construction
**Learning:** Eliminating redundant disk I/O via `lru_cache` and replacing iterative `str.replace` calls with a single-pass `re.sub` using a callback provides a significant performance boost (~4.3x improvement) in LLM-intensive pipelines. Pre-compiling the regex pattern at the module level further reduces overhead.

**Action:** Always use caching for static or semi-static resources like prompt templates. For string templating with multiple variables, prioritize single-pass substitution techniques over iterative replacements. Ensure cache invalidation is handled when source data (e.g., prompt files) changes.
