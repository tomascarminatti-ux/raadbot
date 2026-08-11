# Bolt's Journal: Critical Learnings Only

## 2026-02-25 - Prompt Template Caching with LRU Cache
**Learning:** In a highly iterative pipeline like Raadbot, system prompts and the prompt maestro are loaded repeatedly from disk. Placing a simple `lru_cache` wrapper around `load_prompt` avoids redundant file I/O operations and speeds up prompt preparation dramatically (~4-5x speedup). However, because prompts can be programmatically refined via the API, the cache must be explicitly cleared on refinement to prevent serving stale prompts.
**Action:** Implement `@functools.lru_cache` on `load_prompt` in `agent/prompt_builder.py` and invoke `clear_prompt_caches()` in `api.py` upon any prompt update.
