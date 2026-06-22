## 2026-06-22 - Optimized Prompt Builder with Tiered Caching

**Learning:** Loading prompts from disk and performing multiple iterative string replacements for variable injection is a significant bottleneck in agentic workflows where prompts are built frequently. iterative `.replace()` calls have O(N*M) complexity (N=length, M=variables), while a single-pass regex callback is O(N).

**Action:** Use `functools.lru_cache` for template loading and `re.sub()` with a callback function for efficient single-pass variable injection in templating engines.
