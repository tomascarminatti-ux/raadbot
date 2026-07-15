## 2026-02-21 - Single-pass Regex for Template Building
**Learning:** Using a loop of `str.replace()` for template variable substitution is $O(M \times N)$ and causes multiple string allocations. A single-pass `re.sub()` with a mapping function is $O(N)$ and much more efficient as the number of variables or template size grows.
**Action:** Always prefer `re.sub()` with a callback function for multi-variable template injection.

## 2026-02-21 - Module-level Schema Caching
**Learning:** Loading and parsing JSON schemas from disk inside a class constructor causes redundant I/O for every instance. Moving the `lru_cache` to a module-level helper allows the parsed schema to be shared across all instances of the class.
**Action:** Cache static asset loading (like JSON schemas or prompt templates) at the module level or using a singleton pattern.
