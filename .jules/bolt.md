## 2025-05-15 - [Optimization] Efficient Prompt Templating and Asset Caching

**Learning:** Replacing iterative `.replace()` calls with a single-pass `re.sub()` using a callback function significantly improves performance for multi-variable template injection. Additionally, module-level caching (`lru_cache`) for static disk assets (prompts, schemas) eliminates redundant I/O, which is a common bottleneck in high-throughput LLM pipelines.

**Action:** Always prefer single-pass regex substitution for templating and use module-level caching for any immutable data loaded from disk to ensure minimal overhead in the hot path.
