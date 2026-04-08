## 2025-05-15 - [Prompt Builder Optimization]
**Learning:** Redundant disk I/O and iterative `str.replace` calls in prompt template building can be a significant bottleneck when processing multiple candidates. Using `functools.lru_cache` for template loading and a single-pass `re.sub` for variable injection significantly reduces latency.
**Action:** Always use caching for static or slow-changing assets like prompt templates and prefer single-pass regex replacement over multiple `str.replace` calls for complex templating.
