## 2025-05-05 - Multi-pass string replacement vs single-pass regex
**Learning:** Repeatedly calling `.replace()` on a large string for multiple variables is inefficient as it scans the string and re-allocates it for every replacement ((N \times M)$). Using `re.sub()` with a callback function performs all replacements in a single scan ((M)$).
**Action:** Use a single-pass regex replacement for template interpolation when dealing with multiple variables.

## 2025-05-05 - Template Disk I/O Bottleneck
**Learning:** Reading prompt templates from disk on every execution is a significant bottleneck in a high-concurrency pipeline.
**Action:** Use `functools.lru_cache` to cache template content in memory.
