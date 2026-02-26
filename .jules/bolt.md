# Bolt's Performance Journal ⚡

## 2025-05-15 - [Prompt Construction Optimization]
**Learning:** In multi-agent pipelines where prompt templates are loaded and variables are injected frequently, disk I/O and inefficient string manipulation become significant bottlenecks. The original implementation used a loop with multiple `.replace()` calls and local imports, resulting in $O(N \times M)$ complexity.
**Action:** Use `functools.lru_cache` for template loading to eliminate redundant disk reads. Refactor variable injection to use a single-pass `re.sub()` with a callback, reducing complexity to $O(N)$. Ensure cache invalidation (`cache_clear()`) is implemented in endpoints that modify source templates.

## 2025-05-15 - [Orchestrator Import Issue]
**Learning:** Missing top-level imports in the orchestrator (like `time`) can cause hard-to-detect `NameError` exceptions during the final stages of a pipeline run (e.g., summary generation).
**Action:** Always verify all standard library dependencies are imported at the top level, especially those used in results aggregation.
