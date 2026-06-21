## 2025-05-22 - Optimized prompt building with tiered caching and single-pass injection
**Learning:** Sequential `.replace()` calls on large strings with many variables are O(N*M) where N is string length and M is number of variables. Using a single-pass `re.sub()` with a callback reduces this to O(N). Additionally, disk I/O for prompt templates is a bottleneck in high-concurrency scenarios; `lru_cache` significantly reduces latency.
**Action:** Use tiered template caching and regex callbacks for complex string interpolations to maintain high throughput.
