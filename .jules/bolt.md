## 2026-05-26 - Orchestrator Parallelization & Prompt Optimization
**Learning:** Sequential processing of multiple candidates in LLM pipelines is a major bottleneck. Offloading synchronous LLM calls to threads using `asyncio.to_thread` combined with `asyncio.gather` allows for efficient parallel execution without blocking the async event loop. Additionally, template-heavy prompt construction can be significantly improved by disk I/O caching and single-pass regex substitution.
**Action:** Always parallelize batch-processing loops in orchestrators and use caching for static template files.
