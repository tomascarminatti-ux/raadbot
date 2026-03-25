## 2026-03-25 - Prompt Loading Optimization
**Learning:** The application repeatedly reads system prompts and "maestro" prompts from disk for every GEM step and every candidate. In a parallel execution environment, this leads to redundant I/O.
**Action:** Applied `functools.lru_cache` to `load_prompt` and `load_maestro` in `agent/prompt_builder.py`. This reduced prompt construction time by ~73% in benchmarks.
