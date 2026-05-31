## 2025-05-24 - Single-pass Template Interpolation & I/O Offloading
**Learning:** Sequential str.replace calls on large templates create O(N*M) complexity and many intermediate string objects. Using a single-pass re.sub with a callback is significantly more efficient. Additionally, synchronous file I/O in an async pipeline blocks the entire event loop, increasing latency for all concurrent tasks.
**Action:** Always use re.sub for multi-variable template interpolation and asyncio.to_thread for synchronous file writes in FastAPI/Asyncio environments.
