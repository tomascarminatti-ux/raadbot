## 2026-03-21 - Parallelizing candidate processing in GEM6Orchestrator
**Learning:** Sequential LLM calls in a loop for processing multiple candidates created a significant O(n) bottleneck where n is the number of candidates. Transitioning to an autonomous orchestration model with Gemini 2.0 Flash (asynchronous) allows for high-concurrency processing with minimal overhead.
**Action:** Always favor asynchronous I/O and `asyncio.gather` when processing independent entities (like candidates) through LLM pipelines to maximize throughput.
