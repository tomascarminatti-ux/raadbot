## 2026-05-29 - Optimize build_prompt with single-pass regex and caching
**Learning:** Repeated use of `str.replace` in a loop for template substitution is inefficient ((N \cdot M)$) and causes excessive string allocations. Using `re.sub` with a callback achieves the same result in a single pass ((N)$). Combining this with `functools.lru_cache` for I/O-bound template loading significantly reduces latency.
**Action:** Use regex callbacks for multi-variable template substitution and cache frequently read configuration/template files.
