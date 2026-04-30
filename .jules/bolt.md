## 2025-05-15 - Optimize Prompt Construction Logic
**Learning:** Using `re.sub` with a callback for variable substitution in prompt templates is significantly more efficient than nested loops or multiple `.replace()` calls, especially as the number of variables or the template size increases. Caching static templates with `lru_cache` eliminates redundant disk I/O.
**Action:** Always prefer single-pass substitution and memoization for static resource loading in performance-critical paths.
