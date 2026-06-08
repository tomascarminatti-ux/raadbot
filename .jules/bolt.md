## 2025-05-14 - Optimized Prompt Building with Caching and Single-Pass Regex

**Learning:** String substitution using a loop of `.replace()` calls is $O(N \times M)$ where $N$ is string length and $M$ is the number of variables. In an agentic system with large prompts and many inputs, this becomes a measurable bottleneck. Additionally, redundant disk I/O for static template files adds unnecessary latency.

**Action:** Use `functools.lru_cache` for template loading to eliminate redundant I/O. Use `re.sub` with a callback for single-pass variable substitution, which is $O(N)$ and prevents "nested replacement" bugs.
