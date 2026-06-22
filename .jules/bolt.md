## 2025-05-15 - Single-pass Regex Substitution and Template Caching
**Learning:** Replacing multiple iterative `.replace()` calls with a single-pass `re.sub()` using a callback function improves complexity from O(N*M) to O(N), where N is template length and M is variable count. Combining this with `lru_cache` for file-based templates significantly reduces latency in high-throughput agent pipelines.
**Action:** Use `re.sub(pattern, callback, text)` for template engines and apply `functools.lru_cache` to static file loaders.
