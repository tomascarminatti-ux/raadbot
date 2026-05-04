## 2025-05-04 - Background Persistence Pattern
**Learning:** Synchronous file I/O in an `asyncio` event loop (like FastAPI's) is a major bottleneck that blocks all concurrent operations, including WebSocket broadcasts.
**Action:** Use an `asyncio.Queue` and `asyncio.to_thread` to offload persistent state updates to a background task, ensuring the main loop remains responsive.
