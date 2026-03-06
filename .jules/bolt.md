## 2025-05-14 - Multi-Agent Pipeline Parallelization
**Learning:** Sequential LLM calls in a multi-agent pipeline create a massive bottleneck when processing multiple entities (candidates). Moving to `asyncio.gather` for candidate processing and making the LLM client fully asynchronous allows for concurrent execution, reducing total latency from linear to roughly the duration of the slowest single candidate orchestration.
**Action:** Always favor asynchronous LLM clients and use `asyncio.gather` (with proper task creation) for batch processing in agentic workflows.

## 2025-05-14 - Connection Pooling in Async Clients
**Learning:** Repeatedly instantiating `httpx.AsyncClient` within an async method adds significant overhead due to constant TCP/TLS handshake negotiation.
**Action:** Reuse a single `httpx.AsyncClient` instance stored on the class level (e.g., in `__init__`) to leverage connection pooling and improve throughput for high-frequency API calls.
