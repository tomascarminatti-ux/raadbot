## 2024-05-23 - Sequential Processing Bottleneck
**Learning:** Sequential execution of LLM modules in a pipeline is a major latency bottleneck, especially when processing multiple candidates.
**Action:** Use `asyncio.gather` and `asyncio.to_thread` (for sync clients) to parallelize candidate evaluations.
