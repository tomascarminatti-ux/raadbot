## 2025-05-22 - Optimize prompt building with caching and single-pass replacement
**Learning:** In string-heavy template engines, multiple `.replace()` calls in a loop create a bottleneck (O(N*M)). Using a single-pass `re.sub()` with a callback reduces complexity to O(N). Additionally, disk I/O for static template files can be easily eliminated using `@functools.lru_cache`.
**Action:** Use single-pass regex substitution for template engines and cache static file reads to minimize latency in hot paths.
