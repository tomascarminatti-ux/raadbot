## 2025-05-22 - Optimized prompt building with template caching and single-pass replacement
**Learning:** Redundant file I/O and multiple `.replace()` calls in template processing can be a significant bottleneck. Using `functools.lru_cache` and `re.sub` with a callback allows for much faster template construction.
**Action:** Always check if templates are being re-read from disk on every call and consider single-pass regex replacement for multiple placeholders.
