# Bolt's Performance Journal

## 2025-05-18 - Concurrent candidate context processing in GEM6 Orchestrator
**Learning:** Sequential async processing in candidate batch loops creates a major I/O-bound bottleneck during pipeline execution. Using `asyncio.gather` parallelizes candidate context evaluation, yielding up to an N-fold speedup when processing multiple candidates.
**Action:** When iterating over async workload tasks across multiple independent entities (like candidate profiles), always run them concurrently with `asyncio.gather` or task groups rather than awaiting each task sequentially in a `for` loop.
