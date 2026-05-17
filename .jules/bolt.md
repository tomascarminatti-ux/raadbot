## 2024-05-11 - Optimized Prompt Builder
**Learning:** Repeated disk I/O and iterative string replacement for prompt variables is a significant bottleneck when running parallel agent chains.
**Action:** Use `@lru_cache` for template loading and `re.sub` with a mapping function for single-pass variable injection.

## 2025-05-22 - Optimized Prompt Construction
**Learning:** Loading prompt templates from disk in every `build_prompt` call was slowing down the parallel execution of multiple candidates.
**Action:** Implemented caching for prompt templates and optimized the variable replacement logic using regex, resulting in a ~17.7x speedup.

## 2026-05-17 - Parallel Orchestration with Async Threading
**Learning:** Sequential processing of candidates in `GEM6Orchestrator` combined with blocking synchronous LLM calls (`run_gem`) neutralized the benefits of an `async` pipeline.
**Action:** Parallelized candidate processing using `asyncio.gather` and offloaded blocking `run_gem` calls to threads with `asyncio.to_thread` to ensure true concurrency.
