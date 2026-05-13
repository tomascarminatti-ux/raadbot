## 2026-05-13 - Async/Await Bottleneck in Orchestration
**Learning:** The synchronous `GeminiClient` was blocking the FastAPI event loop during LLM calls (Gemini/Ollama), which take several seconds. This prevented the application from handling other requests (like dashboard updates or concurrent pipelines) efficiently.
**Action:** Always use asynchronous clients (`httpx.AsyncClient`, `client.aio`) for network I/O in FastAPI applications to keep the event loop non-blocking. Use `asyncio.gather` for independent I/O tasks to achieve parallel execution and significant speedup.
