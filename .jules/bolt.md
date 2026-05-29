## 2026-05-29 - Prompt Builder Single-Pass Regex & Caching
**Learning:** Sequential `str.replace()` calls in a loop cause multiple string copies and scans (O(K*N)). Template loading from disk is a frequent bottleneck in high-throughput agent loops.
**Action:** Use `functools.lru_cache` for I/O-bound template loading and `re.sub()` with a callback for single-pass variable replacement (O(N)).
