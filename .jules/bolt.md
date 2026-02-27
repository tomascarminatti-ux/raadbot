## 2025-05-14 - Optimized Prompt Templating
**Learning:** Frequent disk I/O for loading prompt templates and iterative string replacements using `.replace()` for multiple variables created a measurable performance bottleneck (latencies around 0.14ms per prompt). A single-pass `re.sub` with a dictionary-based replacer and `functools.lru_cache` for I/O significantly reduces overhead.
**Action:** Use `lru_cache` for static file loading and implement single-pass regex substitution for templates with multiple variables to minimize string allocations and I/O.
