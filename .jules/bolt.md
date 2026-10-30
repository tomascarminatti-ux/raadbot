## 2026-10-30 - Concurrent candidate processing in GEM6Orchestrator
**Learning:** Sequential `for` loop iteration with `await` in asynchronous pipeline orchestrators causes severe head-of-line blocking across candidate workloads. Converting sequential candidate processing to `asyncio.gather` enables concurrent execution of independent I/O-bound LLM reasoning loops, reducing overall pipeline latency from `O(N * T)` to `O(T)`.
**Action:** Always use `asyncio.gather` for independent candidate or batch tasks in async orchestrators.
