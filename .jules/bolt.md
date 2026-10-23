## 2026-03-31 - File-Backed Template Caching with Automatic Invalidation

**Learning:** Prompt template files in `agent/prompt_builder.py` are loaded repeatedly during LLM pipeline execution. Standard `@functools.lru_cache` can cause stale data when prompt files are dynamically updated on disk (e.g., via `/api/v1/gems/refine`). Passing the file modification timestamp (`os.path.getmtime(filepath)`) as an argument to the cached helper `_load_prompt_cached(filepath, mtime)` provides both LRU memory performance (~5.6x speedup) and automatic cache invalidation whenever a file is saved or refined on disk.

**Action:** Use `(filepath, os.path.getmtime(filepath))` as parameters for `@functools.lru_cache` helpers when caching local file content that can be modified during application runtime.
