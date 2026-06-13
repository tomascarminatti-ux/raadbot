## 2026-06-13 - Parallel Candidate Processing Speedup
**Learning:** In a network-bound application using LLMs, sequential processing of multiple independent entities (candidates) is a significant bottleneck. Refactoring from a for-loop to `asyncio.gather` while offloading synchronous LLM and file I/O operations to `asyncio.to_thread` resulted in a ~2.4x speedup in benchmarks (1.45s down to 0.60s for 10 candidates with 100ms simulated latency).
**Action:** Always prefer concurrent processing for independent entities and ensure that synchronous library calls (like LLM clients or standard file I/O) are offloaded to threads in an `asyncio` environment to prevent event loop blocking.

## 2026-06-13 - Thread-Safe WebSocket Logging
**Learning:** Moving to a concurrent orchestration model requires protecting shared resources like the `pipeline_state.json` file used for real-time dashboard updates. Without protection, concurrent writes from multiple candidate processing tasks can lead to race conditions or file corruption.
**Action:** Use `asyncio.Lock` to synchronize access to shared files when multiple async tasks perform I/O, and continue to use `asyncio.to_thread` for the actual synchronous I/O operations.
