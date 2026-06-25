## 2025-05-15 - [Optimization: Single-pass Regex Substitution and Caching]
**Learning:** Replacing multiple iterative `.replace()` calls with a single-pass `re.sub()` with a callback improves complexity from $O(N \cdot M)$ to $O(N)$, where $N$ is the template length and $M$ is the number of variables. This significantly improves performance for large templates with many variables. Additionally, using `functools.lru_cache` for template loading eliminates redundant disk I/O.
**Action:** Use single-pass regex and caching for any template-based string generation in the future.
