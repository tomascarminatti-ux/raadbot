## 2025-05-24 - [Risk of Local Benchmark Scripts]
**Learning:** Benchmark scripts that write dummy prompt files to the same directory as production prompts (e.g., `prompts/`) can accidentally overwrite critical system prompts if they use production file names like `00_prompt_maestro.md`.
**Action:** Always use unique, non-production filenames (e.g., `test_benchmark_maestro.md`) for temporary files in benchmark scripts, and ensure they are cleaned up after execution.

## 2025-05-24 - [Parallelizing Blocking LLM Calls]
**Learning:** In an async orchestrator, calling a synchronous LLM client directly inside a loop blocks the entire event loop, negating the benefits of `asyncio.gather`.
**Action:** Always wrap synchronous client calls with `asyncio.to_thread` when executing multiple LLM tasks in parallel to ensure true concurrency.
