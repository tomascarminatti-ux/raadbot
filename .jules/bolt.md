## 2026-02-26 - [Optimized prompt construction]
**Learning:** Multiple string substitutions in a loop cause (M \times V)$ complexity and many string copies. Single-pass `re.sub` with a callback reduces this to (M)$. Combined with `lru_cache` for disk I/O, it significantly improves performance in hot paths.
**Action:** Use `re.sub` with a mapping function for multi-variable template injection and `lru_cache` for static resource loading.
