## 2025-06-06 - Parallel Candidate Orchestration
**Learning:** Sequential processing of LLM requests is a major bottleneck in pipelines. Using `asyncio.gather` with `asyncio.to_thread` for synchronous LLM clients allows true concurrent execution.
**Action:** Always offload synchronous I/O or LLM calls to threads when using them inside an async event loop for parallel processing.

## 2025-06-06 - Prompt Builder Optimization
**Learning:** Repeated string replacements and disk I/O in template engines scale poorly. `lru_cache` for files and a single-pass regex for variables significantly reduce latency.
**Action:** Use caching for static/semi-static templates and avoid multiple `.replace()` calls on large strings.
