## 2025-05-15 - [Prompt Builder Optimization]
**Learning:** Replacing iterative `.replace()` calls with a single-pass `re.sub()` using a callback function improves complexity from O(N*M) to O(N), where N is template length and M is variable count. Combined with `lru_cache` for disk I/O, latency for prompt building dropped from ~0.17ms to ~0.02ms (approx. 9x improvement).
**Action:** Use single-pass regex substitution for template engines and cache static/semi-static file reads.
