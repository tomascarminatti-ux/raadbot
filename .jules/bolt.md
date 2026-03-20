# Bolt's Performance Journal

## 2025-05-14 - [Prompt Building Optimization]
**Learning:** Prompt building in a multi-agent system often involves redundant disk reads for static template files. Caching these reads at the application level can significantly reduce overhead, especially in parallel execution loops.
**Action:** Implement memoization using `@functools.lru_cache` for template loading functions and ensure cache invalidation is triggered after any user-initiated template updates.
