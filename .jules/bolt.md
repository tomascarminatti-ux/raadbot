## 2025-05-14 - Optimized Prompt Injection and Caching
**Learning:** Replacing multiple iterative `.replace()` calls with a single-pass `re.sub()` using a callback function improves complexity from O(N*M) to O(N), where N is template length and M is variable count. Combined with `lru_cache` for template loading, latency was reduced by ~8x.
**Action:** Use single-pass regex substitution for templates with multiple variables and implement tiered caching for disk-based templates.
