## 2026-06-15 - [Optimization of Prompt Building and I/O]
**Learning:** Disk I/O in the prompt building hot path (loading templates from disk for every GEM in a pipeline) and blocking synchronous file writes in an async pipeline are significant bottlenecks.
**Action:** Use `functools.lru_cache` for template loading and `re.sub` with a callback for single-pass variable substitution. Offload synchronous file I/O to separate threads using `asyncio.to_thread` to keep the event loop responsive during parallel processing.
