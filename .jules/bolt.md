## 2025-05-15 - Single-pass Regex Substitution
**Learning:** Sequential `.replace()` calls for template variables have O(N*M) complexity (where N is the number of variables and M is the template size) and are prone to accidental recursive replacements if a variable value contains a placeholder for another variable.
**Action:** Use a single-pass `re.sub()` with a callback function for O(M) complexity and guaranteed one-time substitution.

## 2025-05-15 - LRU Cache for File I/O
**Learning:** Loading static templates from disk on every request introduces unnecessary latency and system call overhead, especially under high concurrency.
**Action:** Apply `@functools.lru_cache` to file loading functions for templates that do not change frequently during the application lifecycle.
