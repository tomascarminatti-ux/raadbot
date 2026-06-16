## 2026-06-16 - Performance learning: Async vs Sync I/O in candidate orchestration
**Learning:** Sequential processing of multiple candidates in the orchestrator was a major bottleneck. Offloading synchronous LLM calls and file I/O to threads via `asyncio.to_thread` while using `asyncio.gather` for parallel processing provides significant throughput gains without complex architectural changes.
**Action:** Always favor `asyncio.gather` for independent task execution and protect the event loop from blocking calls using `asyncio.to_thread`.

## 2026-06-16 - Performance learning: Prompt variable substitution
**Learning:** Repeated `str.replace()` calls in a loop for prompt building is inefficient. A single-pass `re.sub` with a callback is much faster as the number of variables grows.
**Action:** Use regex-based substitution for template engines when many variables are involved.

## 2026-06-16 - Performance learning: Disk I/O caching
**Learning:** Loading static prompt templates from disk on every request is an anti-pattern. `lru_cache` provides massive speedups for these static or slowly changing assets.
**Action:** Cache static templates or config files in memory after first load.
