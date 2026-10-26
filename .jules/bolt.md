# Bolt's Performance Journal

## 2026-03-31 - Prompt Template Loading LRU Caching
**Learning:** System prompt files in `prompts/*.md` were previously read synchronously from disk on every `build_prompt` call during multi-step orchestration workflows (e.g. GEM6). Decorating helper `_load_prompt_cached` with `@functools.lru_cache(maxsize=32)` keyed by file path and `mtime` eliminates disk I/O while automatically invalidating when files change on disk (such as via AI prompt refinement endpoints).
**Action:** Use `mtime`-aware `@functools.lru_cache` when caching local file resources that might occasionally be updated at runtime.
